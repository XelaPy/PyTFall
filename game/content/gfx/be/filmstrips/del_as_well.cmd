magick mogrify -format webp -quality 80 -define webp:lossless=false *.jpg
del *.jpg
magick mogrify -format webp -quality 80 -define webp:lossless=false *.jpeg
del *.jpeg
magick mogrify -format webp -quality 80 -define webp:lossless=false *.gif
del *.gif
magick mogrify -format webp -quality 100 -define webp:lossless=true *.png
del *.png

pause