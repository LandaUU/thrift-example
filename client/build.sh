dmd -I. main.d     \
	classifier/ClassifierService.d \
	classifier/classificator_types.d \
	-L-L/usr/local/lib \
	-L-lthriftd
