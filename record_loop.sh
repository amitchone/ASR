echo --- Recording session initialised ---
done=0
while : ; do
  python audio.py
  if [ $? == 1 ]; then
    echo --- Recording session terminated ---
    done=1
  fi
  if [ "$done" -ne 0 ]; then
      break
  fi
done
