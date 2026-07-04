# Git Concepts - My Notes

## Branch
A branch is a separate line of development within the same repository. 
It lets me make changes (add features, fix bugs) without affecting the 
main branch until I'm ready to merge. Think of it like working on a 
draft copy of a document while the original stays untouched.

## Merge Conflict
A merge conflict happens when Git tries to combine two branches that 
have changed the same line(s) of the same file in different ways. 
Git cannot automatically decide which version is correct, so it pauses 
and asks me to manually choose or combine the changes before continuing.

## .gitignore
A file that tells Git which files/folders to never track — like venv/, 
__pycache__/, or .env files containing secrets. Keeps the repo clean 
and avoids pushing unnecessary or sensitive files.

## Pull Request (PR)
A request to merge my branch's changes into another branch (usually 
main), reviewed on GitHub before merging — allows team members to 
review code before it becomes part of the main project.