"""Linear supply as a function of price: Qs(p) = 150 + 10p, slope dQs/dp = 10."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
BLUE,RED,INK,MUTE,GREEN="#2E6DB4","#C0392B","#2D2D2D","#6B6B6B","#2E7D4F"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":INK,
                     "axes.linewidth":1.1,"figure.dpi":170})
fig,ax=plt.subplots(figsize=(6.0,4.1))
p=np.linspace(0,8,100); Q=150+10*p
ax.plot(p,Q,color=RED,lw=2.8,label=r"$Q^{s}(p)=150+10p$",zorder=3)
# rise/run triangle between p=3 and p=5
p0,p1=3,5; q0,q1=150+10*p0,150+10*p1
ax.plot([p0,p1],[q0,q0],color=INK,lw=1.6,zorder=4)
ax.plot([p1,p1],[q0,q1],color=INK,lw=1.6,zorder=4)
ax.plot([p0,p1],[q0,q1],color=GREEN,lw=2.4,ls=(0,(4,2)),zorder=4)
ax.text((p0+p1)/2,q0-7,r"run $=\$2$",ha="center",va="top",fontsize=11,color=INK)
ax.text(p1+0.12,(q0+q1)/2,"rise\n$=20$",ha="left",va="center",fontsize=11,color=INK)
for pp,qq in [(p0,q0),(p1,q1)]:
    ax.plot(pp,qq,"o",color=GREEN,ms=8,zorder=5)
ax.text(5.6,236,r"$\dfrac{dQ^{s}}{dp}=\dfrac{20}{2}=10$",fontsize=14,color=GREEN,
        bbox=dict(boxstyle="round,pad=0.4",fc="white",ec=GREEN,lw=1.3))
ax.text(0.35,206,"the slope is the same\neverywhere on a line",fontsize=10.5,color=MUTE,style="italic")
ax.set_xlabel(r"Price  $p$  (\$ per dozen)"); ax.set_ylabel(r"Quantity supplied  $Q^{s}$")
ax.set_xlim(0,8); ax.set_ylim(140,240)
ax.spines[["top","right"]].set_visible(False)
ax.legend(loc="upper left",frameon=False,fontsize=11.5,borderaxespad=0.6)
fig.tight_layout(); fig.savefig("linear-supply.png",bbox_inches="tight",facecolor="white")
print("wrote linear-supply.png")
