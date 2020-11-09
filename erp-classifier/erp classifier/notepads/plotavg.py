import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

average_steps = [79,23,20]

lower_error    = [79-28,23-10,20-10]
upper_error = [125-78,43-23,39-20]

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("A", fontsize=30)
#plt.xlabel("Experiments", fontsize=10)
#plt.ylabel("Average steps", fontsize=10)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('a.png', dpi=300)
plt.show()



average_steps = [95,58,28]

upper_error    =               [160-95,100-58,45-28]
lower_error    = [95-34 ,58-10 ,28-8]


x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("B", fontsize=30)
#plt.xlabel("Experiments", fontsize=10)
#plt.ylabel("Average steps", fontsize=10)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('b.png', dpi=300)
plt.show()


average_steps = np.asarray((105,55,55))

upper_error    = np.subtract(average_steps,np.asarray((199,95,96)))
lower_error    = np.subtract(np.asarray((10,24,20)),average_steps)

average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("C", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('c.png', dpi=300)
plt.show()



average_steps = np.asarray((90,38,36))

upper_error    = np.subtract(average_steps,np.asarray((145,65,58)))
lower_error    = np.subtract(np.asarray((35,8,15)),average_steps)

average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("D", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('d.png', dpi=300)
plt.show()



average_steps = np.asarray((105,104))

upper_error    = np.subtract(average_steps,np.asarray((199,199)))
lower_error    = np.subtract(np.asarray((20,5)),average_steps)

average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("E", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('e.png', dpi=300)
plt.show()


average_steps = np.asarray((95,90,98))

upper_error    = np.subtract(average_steps,np.asarray((170,155,175)))
lower_error    = np.subtract(np.asarray((20,20,5)),average_steps)

average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("F", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('f.png', dpi=300)
plt.show()


average_steps = np.asarray((98,30,22))

upper_error    = np.asarray((90,25,15))
lower_error    = np.asarray((90,25,15))


average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("G", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('g.png', dpi=300)
plt.show()



average_steps = np.asarray((99,90,60))

upper_error    = np.asarray((98,70,50))
lower_error    = np.asarray((97,70,50))


average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,210)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("H", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,50,100,150,200])
plt.savefig('h.png', dpi=300)
plt.show()


average_steps = np.asarray((99,90,125,305,305,307,300))

upper_error    = np.asarray((50,45,100,240,230,240,250))
lower_error    = np.asarray((50,45,100,240,230,240,250))


average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,610)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("A", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,100,200,300,400,500,600])
plt.savefig('Ax.png', dpi=300)
plt.show()


average_steps = np.asarray((89,108,97,290,302,260,290))

upper_error    = np.asarray((50,65,70,240,230,240,250))
lower_error    = np.asarray((50,65,70,240,230,240,250))


average_steps = average_steps.tolist()

x = range(len(average_steps))
y = average_steps
plt.scatter(x=x, y=y)
plt.ylim(0,610)
plt.xticks(np.arange(0, len(average_steps), 1))
plt.errorbar(x, y, yerr=[lower_error, upper_error], fmt='o')
plt.title("B", fontsize=30)
plt.xticks(fontsize=20, rotation=0)
plt.yticks(fontsize=20, rotation=0)
plt.yticks([0,100,200,300,400,500,600])
plt.savefig('Bx.png', dpi=300)
plt.show()