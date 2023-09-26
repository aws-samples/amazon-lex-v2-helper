mkdir layer
rm -Rf ./layer/*
mkdir ./layer/python
cp -R amazon_lex_helper ./layer/python
cd ./layer
zip -r layer.zip ./python/*
