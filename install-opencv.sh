sudo apt-get remove -y ffmpeg x264 libx264-dev
sudo apt-get update -y
sudo apt-get install -y build-essential checkinstall git pkg-config cmake libpng12-0 libpng12-dev libpng++-dev libpng3 libpnglite-dev libpngwriter0-dev libpngwriter0c2 libfaac-dev libjack-jackd2-dev libjasper-dev libjasper-runtime libjasper1 libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libsdl1.2-dev libtheora-dev libva-dev libvdpau-dev libvorbis-dev libx11-dev libxfixes-dev libxvidcore-dev texi2html yasm zlib1g-dev zlib1g-dbg zlib1g libgstreamer0.10-0 libgstreamer0.10-dev libgstreamer0.10-0-dbg gstreamer0.10-tools gstreamer0.10-plugins-base libgstreamer-plugins-base0.10-dev gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly gstreamer0.10-plugins-bad gstreamer0.10-ffmpeg pngtools libtiff4-dev libtiff4 libtiffxx0c2 libtiff-tools libjpeg8 libjpeg8-dev libjpeg8-dbg libjpeg-prog libavcodec-dev libavcodec52 libavformat52 libavformat-dev libxine1-ffmpeg libxine-dev libxine1-bin libunicap2 libunicap2-dev libdc1394-22-dev libdc1394-22 libdc1394-utils swig python-numpy  libpython2.7 python-dev python2.7-dev libjpeg-progs libjpeg-dev libgtk2.0-0 libgtk2.0-dev gtk2-engines-pixbuf

mkdir ./opencv
cd ./opencv
wget ftp://ftp.videolan.org/pub/videolan/x264/snapshots/last_stable_x264.tar.bz2
tar xjf last_stable_x264.tar.bz2
cd last_stable_x264
./configure --enable-static && make && sudo make install
cd ..
wget http://ffmpeg.org/releases/ffmpeg-0.11.1.tar.gz
tar xzf ffmpeg-0.11.1.tar.gz
cd ffmpeg-0.11.1
./configure --enable-gpl --enable-libfaac --enable-libmp3lame
--enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libtheora
--enable-libvorbis --enable-libx264 --enable-libxvid --enable-nonfree
--enable-postproc --enable-version3 --enable-x11grab && make && sudo make install
cd ..
wget http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.1/OpenCV-2.4.1.tar.bz2
tar xjf OpenCV-2.4.1.tar.bz2
cd OpenCV-2.4.1
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D BUILD_EXAMPLES=ON .. && make && sudo make install
cd ../../..
