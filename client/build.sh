dmd -I. main.d     \
	tutorial/Calculator.d \
	tutorial/tutorial_types.d \
	tutorial/tutorial_constants.d     \
	share/SharedService.d share/shared_types.d     \
	-L-L/usr/local/lib \
	-L-lthriftd
