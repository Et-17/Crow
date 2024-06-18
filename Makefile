objs := bin/obj/crow.o bin/obj/eph_reader.o
bin/crow: $(objs)
	cc $(objs) -o ./bin/crow

bin/obj/crow.o: source/main.c
	cc -c ./source/main.c -o ./bin/obj/crow.o

bin/obj/eph_reader.o: source/eph_reader/eph_reader.c
	cc -c ./source/eph_reader/eph_reader.c -o ./bin/obj/eph_reader.o

