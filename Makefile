PREFIX	=/opt
BINDIR	=${PREFIX}/bin

TARGETS	=all clean clobber check distclean install uninstall
TARGET	=all

.PHONY:	${TARGETS}

all::

${TARGETS}::

distclean clobber:: clean

check::	bp.py
	python bp.py ${ARGS}

install:: bp.py
	install -D bp.py ${BINDIR}/bp

uninstall::
	${RM} ${BINDIR}/bp
