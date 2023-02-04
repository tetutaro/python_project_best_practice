Plug 'plytophogy/vim-virtualenv'
Plug 'prabirshrestha/asyncomplete.vim'
Plug 'prabirshrestha/async.vim'
Plug 'prabirshrestha/vim-lsp'
Plug 'prabirshrestha/asyncomplete-lsp.vim'
Plug 'w0rp/ale'
let g:python_host_prog = $VIRTUAL_ENV . '/bin/python3'
let g:python_pylsp_prog = $VIRTUAL_ENV . '/bin/pylsp'
let g:python_flake8_prog = $VIRTUAL_ENV . '/bin/flake8'
augroup PythonLanguageServer
    if executable(g:python_pylsp_prog)
        autocmd!
        autocmd User lsp_setup call lsp#register_server({
            \ 'name': 'pylsp',
            \ 'cmd': {server_info -> [g:python_pylsp_prog]},
            \ 'whitelist': ['python'],
            \ 'workspace_config': {
                \ 'pylsp': {
                    \ 'plugins': {
                        \ 'pycodestyle': {
                            \ 'enabled': v:false,
                        \ },
                        \ 'pyflakes': {
                            \ 'enabled': v:false,
                        \ },
                        \ 'rope_completion': {
                            \ 'enabled': v:false,
                        \ },
                        \ 'yapf': {
                            \ 'enabled': v:false,
                        \ },
                        \ 'flake8': {
                            \ 'enabled': v:true,
                            \ 'executable': g:python_flake8_prog
                        \ }
                    \ }
                \ }
            \ }
        \ })
    endif
augroup END
let g:ale_python_flake8_executable = g:python_host_prog
let g:ale_linters = {
    \ 'python': ['flake8'],
    \ }
let g:ale_lint_on_enter = 1
let g:ale_lint_on_insert_leave = 0
let g:ale_lint_on_save = 1
let g:ale_lint_on_text_changed = 0
let g:ale_fixers = {
    \ 'python': ['black'],
    \ }
let g:ale_fix_on_save = 1
