# Runbook for the first real run of test-strength-gate

This repository exists to run test-strength-gate as a step in a real GitHub workflow for the first time. The branch `demo-pr` changes `src/shopcalc/prices.py` and adds three tests, and the gate should label them as follows.

| Test | Expected verdict | Why |
| --- | --- | --- |
| `test_discount_over_100_percent_is_free` | STRONG | At base, a 150% discount gives -40, so the assertion fails. |
| `test_ten_percent_discount` | WEAK | A 10% discount already worked at base, so the test passes there. |
| `test_format_price` | INCONCLUSIVE | `format_price` doesn't exist at base, so the import fails. |

The workflow is `.github/workflows/tsg.yml`. It runs on `pull_request` only, checks out with `fetch-depth: 2`, installs Python 3.12 and this project, and uses `adamisom/test-strength-gate` pinned to commit `0f2d9d15b7227be6ee34b70dfc9c6a0ab15d1c81`, which is `main` on GitHub as of 9/28/26. A second job runs the plain test suite.

## 1. Check the verdicts locally first

These commands were run on 9/28/26 and gave exactly the three verdicts above, both with `--base main --head demo-pr` and on a depth 2 clone of a merge commit, which is what `actions/checkout` gives on `pull_request`.

```sh
cd ~/dev/tsg-demo
~/dev/test-strength-gate/.venv/bin/python -m test_strength_gate --repo . --base main --head demo-pr
```

## 2. Let the workflow reach the action

While `adamisom/test-strength-gate` is private, a workflow in another repository can't use it. There are two ways to fix that, and each one is a separate decision.

- Make `test-strength-gate` public. Then the demo repository can be public or private.
- Keep it private and allow repositories owned by `adamisom` to use it. GitHub shares actions from a private repository with the owner's other private repositories, so create the demo repository as private in this case.

```sh
gh api -X PUT repos/adamisom/test-strength-gate/actions/permissions/access -f access_level=user
gh api repos/adamisom/test-strength-gate/actions/permissions/access   # should print "access_level":"user"
```

To undo the second option later, run the same PUT with `-f access_level=none`.

## 3. Create the repository and push

```sh
cd ~/dev/tsg-demo
gh auth status
gh repo create adamisom/tsg-demo --private --source . --remote origin
git push -u origin main
git push -u origin demo-pr
```

Use `--public` instead of `--private` if `test-strength-gate` is public by then.

## 4. Open the pull request and watch the run

```sh
gh pr create --repo adamisom/tsg-demo --base main --head demo-pr \
  --title "Clamp discounts to 0 to 100 percent and add format_price" \
  --body "Demo PR for test-strength-gate. Expected verdicts: one strong, one weak, one inconclusive."
gh pr checks --repo adamisom/tsg-demo --watch
gh run list --repo adamisom/tsg-demo --workflow tsg.yml
gh run view --repo adamisom/tsg-demo --log      # pick the run; the log has the markdown report
gh run view --repo adamisom/tsg-demo --web      # opens the run page with the job summary
```

## 5. What to check

In the run's job summary, under the `test-strength` job:

- The heading "Test strength gate" and the line "3 new tests: 1 strong, 1 weak (passes without the source change), 1 inconclusive".
- Base is the tip of `main` and head is the merge commit GitHub built, not the `demo-pr` commit itself. The line should say one changed test file and one changed Python source file.
- The three rows match the table at the top of this file. The strong reason quotes `assert -40.0 == 0`, and the inconclusive reason names the ImportError for `format_price`.

In the annotations:

- The run page lists one warning titled "Weak test" for `tests/test_prices.py::test_ten_percent_discount`, and the PR's Files tab shows the same warning on `tests/test_prices.py`.
- There are no other annotations from the gate, and no error that says HEAD is not a merge commit.

In the checks:

- Both jobs pass. With `fail-on: none`, a weak test doesn't fail the step.
- The "Install test-strength-gate" step installed the package from the pinned commit without errors.

If all of that holds, the README of `test-strength-gate` can say that the Action has run in a real workflow, with a link to this run. Until then it must not say so.

## 6. Optional follow-ups

- Change `fail-on: none` to `fail-on: weak` in a second commit on `demo-pr`, push it, and check that the `test-strength` job fails because of the weak test.
- After new commits to `test-strength-gate` are pushed, update the pinned sha in `tsg.yml` to the new `main`.
