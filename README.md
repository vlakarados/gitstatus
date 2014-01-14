# GitStatus

Package for monitoring changed files and state of the project.
Made as a light alternative to SublimeGit

### Installation

##### Using [Package Control](https://sublime.wbond.net/)

+ Simply open up the command palette (`CTRL+SHIFT+P` or `CMD+SHIFT+P`).
+ Find `Package Control: Install Package`.
+ Search for `GitStatus`

##### Manual

+ Clone to `Packages/` directory

### Usage

By now you should already see repository status updates in your status bar like `Git: Dirty` or `Git: Clean`.

You have two more commands at your disposal from the command palette:


##### Git: Changed files

Shows all created (unstaged), modified, deleted and unmerged files with their corresponding status and path.


##### Git: Unmerged files

Same as above but shows only unmerged ones, this helps merging files without alt-tabbing to your console just to see the files that need to be merged.


### Contributing

If you find bugs please post them in the issues section and/or submit pull requests.
