TARGET      := IlluminateX_Store
APPID       := ILSTORE01
CONTENTID   := UP0000-${APPID}_00-0000000000000001

CC          := ppu-gcc
CFLAGS      := -O2 -Wall -mcpu=cell -I$(PS3DEV)/ppu/include -I$(PSL1GHT)/ppu/include -I$(PS3DEV)/portlibs/ppu/include
LDFLAGS     := -L$(PS3DEV)/ppu/lib -L$(PSL1GHT)/ppu/lib -L$(PS3DEV)/portlibs/ppu/lib -lsysfs -lsysutil -lio -lrt -lm

OBJS        := source/main.o

all: $(TARGET).pkg

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET).elf: $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $@

$(TARGET).self: $(TARGET).elf
	# Using the C tool on GitHub because it actually works there
	make_self $(TARGET).elf $(TARGET).self --npdrm

$(TARGET).pkg: $(TARGET).self assets/PARAM.SFO assets/ICON0.PNG
	mkdir -p pkg/USRDIR
	cp $(TARGET).self pkg/USRDIR/EBOOT.BIN
	cp assets/ICON0.PNG pkg/ICON0.PNG
	cp assets/PARAM.SFO pkg/PARAM.SFO
	# Run pkg.py locally
	./pkg.py --contentid $(CONTENTID) pkg/ $(TARGET).pkg
	rm -rf pkg

clean:
	rm -f $(OBJS) $(TARGET).elf $(TARGET).self $(TARGET).pkg
