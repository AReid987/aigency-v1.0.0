const fs = require('node:fs')
const path = require('node:path')

const packages = fs.readdirSync(path.resolve(__dirname, 'packages'))
const apps = fs.readdirSync(path.resolve(__dirname, 'apps'))

module.exports = {
    prompt: {
        scopes: [...packages, ...apps],
        enableMultipleScopes: true, 
        scopeEnumSeparator: ","
    }
}