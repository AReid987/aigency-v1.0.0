/*
 * File: lint-staged.config.js                                                 *
 * Project: @xprt/xprt-commit                                                  *
 * Created Date: Fr Apr 2025                                                   *
 * Author: <<author>                                                           *
 * -----                                                                       *
 * Last Modified: Fri Apr 11 2025                                              *
 * Modified By: Antonio J. Reid                                                *
 * -----                                                                       *
 * Copyright (c) 2025 10xAigency                                               *
 * -----                                                                       *
 * HISTORY:                                                                    *
 * Date      	By	Comments                                                   *
 * ----------	---	---------------------------------------------------------  *
 */



// lint-staged config for xprt-commit
// Runs linters/formatters only on staged files of matching type
// JS/TS: eslint + prettier; Python: black
// Adjust commands as needed for your project

module.exports = {
  // Lint and format JS/TS files before commit
  "*.{js,jsx,ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  // Format Python files with black before commit
  "*.py": [
    "black --check"
  ]
};