echo 'test1' > test1
echo 'test2' > test2

echo 'testing extension tar...'
./burr.py pack a.tar test1 test2
./burr.py list a.tar
rm test1 test2
./burr.py unpack a.tar
rm a.tar

echo 'testing extension tar.gz...'
./burr.py pack a.tar.gz test1 test2
./burr.py list a.tar.gz
rm test1 test2
./burr.py unpack a.tar.gz
rm a.tar.gz

echo 'testing extension tgz...'
./burr.py pack a.tgz test1 test2
./burr.py list a.tgz
rm test1 test2
./burr.py unpack a.tgz
rm a.tgz

echo 'testing extension gz...'
./burr.py pack a.gz test1
./burr.py list a.gz
rm test1
./burr.py unpack a.gz
rm a.gz

rm test1 test2