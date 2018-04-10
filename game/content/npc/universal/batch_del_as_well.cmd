setlocal
cd /d %~dp0

for /r /d %%a in (*) do mogrify -format webp -quality 100 -define webp:lossless=true "%%~a\*.png"
del /S *.png

for /r /d %%a in (*) do mogrify -format webp -quality 80 -define webp:lossless=false "%%~a\*.jpg"
del /S *.jpg

for /r /d %%a in (*) do mogrify -format webp -quality 80 -define webp:lossless=false "%%~a\*.jpeg"
del /S *.jpeg

pause



