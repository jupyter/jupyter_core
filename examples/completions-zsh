#compdef jupyter
# A zsh autocompleter for jupyter.
_jupyter() {
  IFS=$'\n'

  local context curcontext="$curcontext" state line
  typeset -A opt_args

  local ret=1

  _arguments -C \
    '1: :_jupyter_cmds' \
    '(-h,--help)'{-h,--help}'[Show this help message and exit.]' \
    '--version[Show the jupyter command'\''s version and exit.]' \
    '--config-dir[Show Jupyter config dir.]' \
    '--data-dir[Show Jupyter data dir.]' \
    '--runtime-dir[Show Jupyter runtime dir.]' \
    '--paths[Show all Jupyter paths. Add --json for machine-readable format.]' \
    '--json[Output paths as machine-readable json.]' \
    '*::arg:->args' \
  && ret=0

  case $state in
    (args)
      curcontext="${curcontext%:*:*}:jupyter-cmd-$words[1]:"
      local update_policy
      zstyle -s ":completion:${curcontext}:" cache-policy update_policy
      [[ -z "$update_policy" ]] && \
        zstyle ":completion:${curcontext}:" \
        cache-policy _jupyter_options_caching_policy
      local cache_id=jupyter_options
      local subcmd=$line[1]
      if (_cache_invalid $cache_id || ! _retrieve_cache $cache_id || \
        [[ ${(P)+subcmd} -eq 0 ]] || _cache_invalid $cache_id); then
        typeset -agU $subcmd
        set -A $subcmd $( (jupyter $subcmd --help-all | \
          grep -o '^--[^-][^= ]\+=\?' | sed 's/\([^=]*\)\(=\?\)/(\1)\1\2:/') 2>/dev/null)
        _store_cache $cache_id $subcmd
      fi
      case $subcmd in
        (console)
          _arguments \
            '1:Source file:_files -g "*.py"' \
            ${(P)subcmd} && ret=0
          ;;
        (kernelspec)
          sub2cmd=$line[2]
          case $sub2cmd in
            (install|list)
              if ([[ ${(P)+sub2cmd} -eq 0 ]]) && ! _retrieve_cache $cache_id; then
                typeset -agU $sub2cmd
                set -A $sub2cmd $(_jupyter_get_options $subcmd $sub2cmd)
                _store_cache $cache_id $sub2cmd
              fi
              _arguments "1: :_${subcmd}_cmds" ${(P)sub2cmd} && ret=0
              ;;
            *)
              _arguments "1: :_${subcmd}_cmds" ${(P)subcmd} && ret=0
              ;;
          esac
          ;;
        (nbconvert)
          _arguments \
            '1:Source file:_files -g "*.ipynb"' \
            ${(P)subcmd} && ret=0
          ;;
        (nbextension)
          sub2cmd=$line[2]
          case $sub2cmd in
            (disable|enable)
              if ([[ ${(P)+sub2cmd} -eq 0 ]]) && ! _retrieve_cache $cache_id; then
                typeset -agU $sub2cmd
                set -A $sub2cmd $(_jupyter_get_options $subcmd $sub2cmd)
                _store_cache $cache_id $sub2cmd
              fi
              _arguments \
                '1: :_nbextension_cmds' \
                '2:Extension path:_files' \
                ${(P)sub2cmd} && ret=0
              ;;
            (install)
              if ([[ ${(P)+sub2cmd} -eq 0 ]]) && ! _retrieve_cache $cache_id; then
                typeset -agU $sub2cmd
                set -A $sub2cmd $(_jupyter_get_options $subcmd $sub2cmd)
                _store_cache $cache_id $sub2cmd
              fi
              _arguments \
                '1: :_nbextension_cmds' \
                '2:Extension path:_files' \
                ${(P)sub2cmd} && ret=0
              ;;
            *)
              _arguments "1: :_${subcmd}_cmds" ${(P)subcmd} && ret=0
              ;;
          esac
          ;;
        (notebook)
          sub2cmd=$line[2]
          case $sub2cmd in
            (list)
              if ([[ ${(P)+sub2cmd} -eq 0 ]]) && ! _retrieve_cache $cache_id; then
                typeset -agU $sub2cmd
                set -A $sub2cmd $(_jupyter_get_options $subcmd $sub2cmd)
                _store_cache $cache_id $sub2cmd
              fi
              _arguments "1: :_${subcmd}_cmds" ${(P)sub2cmd} && ret=0
              ;;
            *)
              _arguments "1: :_${subcmd}_cmds" ${(P)subcmd} && ret=0
              ;;
          esac
          ;;
        (trust)
          _arguments \
            '*:Source file:_files -g "*.ipynb"' \
            ${(P)subcmd} && ret=0
          ;;
        *)
          _arguments ${(P)subcmd} && ret=0
          ;;
      esac
    ;;
  esac
}

_jupyter_options_caching_policy() {
  local -a newer
  # rebuild if cache does not exist or is more than a week old
  newer=( "$1"(Nmw-1) )
  return $#newer
}

_jupyter_get_options() {
  echo '(--help)--help[Print help about subcommand.]:'
  (jupyter "$@" --help-all | \
    grep -o '^--[^-][^= ]\+=\?' | sed 's/\([^=]*\)\(=\?\)/(\1)\1\2:/') 2>/dev/null
}

_jupyter_cmds() {
  local -a commands
  if whence jupyter-console >/dev/null; then
    commands=($commands 'console:Launch a Console application inside a terminal.')
  fi
  if whence jupyter-kernelspec >/dev/null; then
    commands=($commands 'kernelspec:Manage Jupyter kernel specifications.')
  fi
  if whence jupyter-nbconvert >/dev/null; then
    commands=($commands 'nbconvert:Convert notebook files to various other formats.')
  fi
  if whence jupyter-nbextension >/dev/null; then
    commands=($commands 'nbextension:Work with Jupyter notebook extensions.')
  fi
  if whence jupyter-notebook >/dev/null; then
    commands=($commands 'notebook:Launch a Tornado based HTML Notebook Server.')
  fi
  if whence jupyter-qtconsole >/dev/null; then
    commands=($commands 'qtconsole:Launch a Console-style application using Qt.')
  fi
  if whence jupyter-trust >/dev/null; then
    commands=($commands 'trust:Sign Jupyter notebooks with your key, to trust their dynamic output.')
  fi
  _describe -t commands 'jupyter command' commands "$@"
}

_kernelspec_cmds() {
  local commands; commands=(
    'help:Print help about subcommand.'
    'install:Install a kernel specification directory.'
    'list:List installed kernel specifications.'
  )
  _describe -t commands 'kernelspec command' commands "$@"
}

_nbextension_cmds() {
  local commands; commands=(
    'help:Print help about subcommand.'
    'enable:Enable a notebook extension.'
    'install:Install notebook extensions.'
    'disable:Disable a notebook extension.'
  )
  _describe -t commands 'nbextension command' commands "$@"
}

_notebook_cmds() {
  local commands; commands=(
    'help:Print help about subcommand.'
    'list:List currently running notebook servers in this profile.'
  )
  _describe -t commands 'notebook command' commands "$@"
}

_jupyter "$@"
# vim: ft=zsh sw=2 ts=2 et
