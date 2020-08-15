PS1_old="$(echo $PS1 | sed -En 's/(.+)\\e](.+)/\1\\\\e]\2/g; s/(.+ )(.+)/\1\\n\2/p')";
_PS1='\[\e]0;$WTITLE: \w\a\]';_PS1+="$PS1_old ";export PS1=$_PS1;
export WTITLE="CAPscript 1.0.0"

if [ -e "$1" ]
then
    python3 CAPscript.py "$1"
else
    python3 CAPscript.py
fi
