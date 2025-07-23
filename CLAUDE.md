# Claude Code Usage Notes

## Project Structure
This repository contains a Flask-based web application for product management and pricing.

## Development

### Scratch Directory
- Use the `scratch/` directory for one-off debugging scripts and temporary files
- `scratch/` is gitignored, so it's safe for experimentation
- Claude can create and run scripts in `scratch/` for debugging

### Development Workflow
- Always do work on a new branch, not main
- When working on a ticket, put the ticket number in commit message and PR
- Run `make test` and `make lint` before any commits to ensure code quality and pass all tests
- When user says "Review time":
  a. Make sure we're not on main branch
  b. Commit what we've done
  c. Push to remote
  d. Create a PR with `gh`
- When user says "made suggestions on the pr":
  - Get PR comments with `gh api repos/OWNER/REPO/pulls/PULL_NUMBER/comments`
  - Address those comments
  - Watch out for multiple PR comments on one code line
- When user says "merge", do a gh pr merge with a merge commit and use the option to delete local and remote branches
- When we merge via gh, it deletes the branch on remote AND LOCAL and checks out main for us

## Testing
- After making changes to Flask app, test by running `make dev` and testing in browser
- Test authentication flows: registration, sign-in, logout
- Check members area functionality
- Verify error handling for invalid inputs and network issues

## Code Style
- Use comments sparingly to explain intent (answer "why") for future readers
- Avoid comments that explain what Claude is doing or what the code does
- Comments should add value, not state the obvious
- Follow existing patterns in the codebase for consistency