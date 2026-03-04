" Healthsites API Client - Neovim/Vim configuration
" Made with love by Kartoza | https://kartoza.com

" Project-specific keybindings under <leader>p
" Assumes which-key is available

lua << EOF
local wk = require("which-key")

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
EOF
