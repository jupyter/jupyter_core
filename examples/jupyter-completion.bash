# load with: . jupyter-completion.bash
#
# NOTE: with traitlets>=5.8, jupyter and its subcommands now directly support
# shell command-line tab-completion using argcomplete, which has more complete
# support than this script. Simply install argcomplete and activate global
# completion by following the relevant instructions in:
# https://kislyuk.github.io/argcomplete/#activating-global-completion

if [[ -n ${ZSH_VERSION-} ]]; then
    autoload -Uz bashcompinit && bashcompinit
fi

_jupyter_get_flags()
{
    local url=$1
    local var=$2
    local dash=$3
    if [[ "$url $var" == $__jupyter_complete_last ]]; then
        opts=$__jupyter_complete_last_res
        return
    fi

    if [ -z $1 ]; then
        opts=$(jupyter --help | sed -n  's/^  -/-/p' |sed -e 's/, /\n/' |sed -e 's/\(-[[:alnum:]_-]*\).*/\1/')
    else
    # matplotlib and profile don't need the = and the
    # version without simplifies the special cased completion
        opts=$(jupyter ${url} --help-all | grep -E "^-{1,2}[^-]" | sed -e "s/<.*//" -e "s/[^=]$/& /" -e "$ s/^/\n-h\n--help\n--help-all\n/")
    fi
    __jupyter_complete_last="$url $var"
    __jupyter_complete_last_res="$opts"
}

_jupyter()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    local prev=${COMP_WORDS[COMP_CWORD - 1]}
    local subcommands="notebook qtconsole console nbconvert kernelspec trust "
    local opts="help"
    local mode=""
    for i in "${COMP_WORDS[@]}"; do
        [ "$cur" = "$i" ] && break
        if [[ ${subcommands} == *${i}* ]]; then
            mode="$i"
            break
        elif [[ ${i} == "--"* ]]; then
            mode="nosubcommand"
            break
        fi
    done


    if [[ ${cur} == -* ]]; then
        case $mode in
            "notebook" | "qtconsole" | "console" | "nbconvert")
                _jupyter_get_flags $mode
                opts=$"${opts}"
                ;;
            "kernelspec")
                if [[ $COMP_CWORD -ge 3 ]]; then
                    # 'history trim' and 'history clear' covered by next line
                    _jupyter_get_flags $mode\ "${COMP_WORDS[2]}"
                else
                    _jupyter_get_flags $mode

                fi
                opts=$"${opts}"
                ;;
            *)
                _jupyter_get_flags
        esac
        # don't drop the trailing space
        local IFS=$'\t\n'
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    elif [[ $mode == "kernelspec" ]]; then
        if [[ $COMP_CWORD -ge 3 ]]; then
            # drop into flags
            opts="--"
        else
            opts="list 	install "
        fi
        local IFS=$'\t\n'
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    else
        if [ "$COMP_CWORD" == 1 ]; then
            local IFS=$'\t\n'
            local sub=$(echo $subcommands | sed -e "s/ / \t/g")
            COMPREPLY=( $(compgen -W "${sub}" -- ${cur}) )
        else
            local IFS=$'\n'
            COMPREPLY=( $(compgen -o filenames -f -- ${cur}) )
        fi
    fi

}
complete -o default -o nospace -F _jupyter jupyter
