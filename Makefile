include config.mk

TXT_FILES=$(wildcard *.txt)
DAT_FILES=$(patsubst %.txt, %.dat, $(TXT_FILES))
STAT_DAT_FILES = $(wildcard *_stat.dat)


.PHONY : dats
dats: $(DAT_FILES)

%.dat : %.txt counter.py
	$(COUNT) -f $< -o $*_stat.dat

archive : $(DAT_FILES) $(COUNTER)
	$(ARCHIVE) $(ARCHIVE_NAME)  $(STAT_DAT_FILES)

.PHONY: clean
clean:
	rm -f $(STAT_DAT_FILES)
	rm -f $(ARCHIVE_NAME)


