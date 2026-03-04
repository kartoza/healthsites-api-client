-- Healthsites API Client - Neovim project configuration
-- Made with love by Kartoza | https://kartoza.com

-- Set Python path for LSP
vim.g.python3_host_prog = vim.fn.expand("~/.venv/bin/python3")

-- Project-specific settings
vim.opt_local.tabstop = 4
vim.opt_local.shiftwidth = 4
vim.opt_local.expandtab = true

-- Configure LSP for Python
local lspconfig = require("lspconfig")
if lspconfig.pyright then
    lspconfig.pyright.setup({
        settings = {
            python = {
                analysis = {
                    typeCheckingMode = "basic",
                    autoSearchPaths = true,
                    useLibraryCodeForTypes = true,
                },
            },
        },
    })
end

-- Configure formatters
if vim.fn.executable("black") == 1 then
    vim.api.nvim_create_autocmd("BufWritePre", {
        pattern = "*.py",
        callback = function()
            vim.lsp.buf.format({ async = false })
        end,
    })
end

-- Project keybindings using which-key
local ok, wk = pcall(require, "which-key")
if ok then
    wk.add({
        { "<leader>p", group = "Project" },
        { "<leader>pr", "<cmd>!python -m pytest tests/ -v<cr>", desc = "Run Tests" },
        { "<leader>pf", "<cmd>!black healthsites/ tests/ && ruff check --fix healthsites/ tests/<cr>", desc = "Format Code" },
        { "<leader>pl", "<cmd>!ruff check healthsites/ tests/<cr>", desc = "Lint Code" },
        { "<leader>pt", "<cmd>!mypy healthsites/<cr>", desc = "Type Check" },
        { "<leader>pd", "<cmd>!mkdocs serve &<cr>", desc = "Serve Docs" },
        { "<leader>pb", "<cmd>!mkdocs build<cr>", desc = "Build Docs" },
        { "<leader>pe", "<cmd>e examples/list_endpoints.py<cr>", desc = "Open Example" },
        { "<leader>pc", "<cmd>e healthsites/client.py<cr>", desc = "Open Client" },
    })
end

print("Healthsites API Client project loaded")
