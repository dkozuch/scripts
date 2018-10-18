CXX=g++

MainLSI: MainLSI.o Positions.o FindHbonds.o LocalStructureIndex.o
	$(CXX) -o $@ $^ -lm

clean:
	rm *.o
