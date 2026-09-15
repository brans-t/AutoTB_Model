## MgNb2(PO5)2 · 对称性报告

结构：[POSCAR](<POSCAR>) · 磁矩：[magnetic_config.json](<magnetic_config.json>)

### 群判定

| 群 | 判定结果 | 状态与来源 | 操作数 |
|:---:|:---:|:---:|:---:|
| 普通空间群 | **P-4 (No. 81)**；点群 -4；Hall P -4 (No. 355) | spglib；已识别 | 4 |
| 磁空间群 | **BNS 81.35；UNI 695**；类型 3 | spglib；已识别 | 4 |
| 定向自旋空间群 | **OSSG 81.3.1.1.L**；$P \overline{1}\mid \overline{4} \infty_{001}m\mid 1$ | ok；FindSpinGroup 识别，spinspg 操作 | 4 |

OSSG 后端原始符号：`"P -1|-4 ∞_{001}m|1"`。
自旋点群（后端记号）：`∞/mm`。
识别后端：findspingroup；操作后端：spinspg。
群构成：$G_0$ 为 P-4 (No. 81)；$L_0$ 为 P2 (No. 3)；MSG 为 P-4' (BNS 81.35)。
磁相（后端标签）：AFM(Altermagnet)。

No. 是普通空间群编号；BNS、UNI 是磁空间群编号；OSSG 是定向自旋空间群索引。

### 交替磁相关操作

**交替磁初步候选。**下列非平凡空间操作连接异号自旋位点；磁结构共线且补偿，纯平移与反演没有连接异号自旋位点。

| 关键操作 | 类型 | 位点映射 | 匹配自旋操作 |
|:---:|:---:|:---:|:---:|
| **#2** | $\bar{4}$（$S_{4}$） | 14 $\rightarrow$ 15 | 已验证自旋翻转 |
| **#4** | $\bar{4}$（$S_{4}$） | 14 $\rightarrow$ 15 | 已验证自旋翻转 |

操作矩阵见下文同序号群操作；判定只给出对称性候选，不代表能带劈裂已被计算。

### 晶体对称性

晶格矩阵（行矢量，Å）：

$$
A_{\mathrm{rows}}=\begin{pmatrix}6.6163409 & 1.865535\times 10^{-9} & 0 \\ -1.865535\times 10^{-9} & 6.6163409 & 0 \\ 0 & 0 & 20\end{pmatrix}
$$

16 个原子；7 个对称性不等价位点。

| 原子索引 | 元素 | 分数坐标 | 等价原子代表 | Wyckoff |
|:---:|:---:|:---:|:---:|:---:|
| 0 | O | $\left(0.00027123508,\;0.81857874,\;0.54925434\right)$ | 0 | h |
| 1 | O | $\left(0.99972877,\;0.18142126,\;0.54925434\right)$ | 0 | h |
| 2 | O | $\left(0.81857874,\;0.99972877,\;0.45074566\right)$ | 0 | h |
| 3 | O | $\left(0.18142126,\;0.00027123508,\;0.45074566\right)$ | 0 | h |
| 4 | O | $\left(0.30824793,\;0.49962881,\;0.54518994\right)$ | 4 | h |
| 5 | O | $\left(0.69175204,\;0.50037119,\;0.54518994\right)$ | 4 | h |
| 6 | O | $\left(0.49962881,\;0.69175204,\;0.45481006\right)$ | 4 | h |
| 7 | O | $\left(0.50037119,\;0.30824793,\;0.45481006\right)$ | 4 | h |
| 8 | O | $\left(0,\;0.5,\;0.42725004\right)$ | 8 | g |
| 9 | O | $\left(0.5,\;0,\;0.57274996\right)$ | 8 | g |
| 10 | Mg | $\left(0,\;0,\;0.36454498\right)$ | 10 | e |
| 11 | Mg | $\left(0,\;0,\;0.63545499\right)$ | 10 | e |
| 12 | P | $\left(0,\;0,\;0.5\right)$ | 12 | a |
| 13 | P | $\left(0.5,\;0.5,\;0.5\right)$ | 13 | c |
| 14 | Nb | $\left(0,\;0.5,\;0.51502238\right)$ | 14 | g |
| 15 | Nb | $\left(0.5,\;0,\;0.48497762\right)$ | 14 | g |

### 群操作

#### 普通空间群操作
共 4 个。$R$ 和 $\mathbf{t}$ 作用于分数坐标。

**操作 #1** · $E$

$$
R_{1}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{1}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

**操作 #2** · $\bar{4}$（$S_{4}$）

$$
R_{2}=\begin{pmatrix}0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{2}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

**操作 #3** · $C_{2}$

$$
R_{3}=\begin{pmatrix}-1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{3}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

**操作 #4** · $\bar{4}$（$S_{4}$）

$$
R_{4}=\begin{pmatrix}0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{4}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

#### 磁空间群操作
共 4 个。$R$ 和 $\mathbf{t}$ 作用于分数坐标。

**操作 #1**

$$
R_{1}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{1}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

时间反演：否。

**操作 #2**

$$
R_{2}=\begin{pmatrix}0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{2}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

时间反演：是。

**操作 #3**

$$
R_{3}=\begin{pmatrix}-1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{3}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

时间反演：否。

**操作 #4**

$$
R_{4}=\begin{pmatrix}0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{4}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

时间反演：是。

#### 自旋空间群操作
共 4 个。$R$ 和 $\mathbf{t}$ 作用于分数坐标。
$S$ 是笛卡尔自旋旋转矩阵。

**操作 #1**

$$
R_{1}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{1}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

$$
S_{1}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{pmatrix}
$$

**操作 #2**

$$
R_{2}=\begin{pmatrix}0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{2}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

$$
S_{2}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & -1\end{pmatrix}
$$

**操作 #3**

$$
R_{3}=\begin{pmatrix}-1 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 1\end{pmatrix},\qquad \mathbf{t}_{3}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

$$
S_{3}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{pmatrix}
$$

**操作 #4**

$$
R_{4}=\begin{pmatrix}0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix},\qquad \mathbf{t}_{4}=\begin{pmatrix}0 \\ 0 \\ 0.99999997\end{pmatrix}
$$

$$
S_{4}=\begin{pmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & -1\end{pmatrix}
$$

### 磁结构与对称性

非零原子磁矩（笛卡尔坐标；未列出的原子磁矩为零）：

| 原子索引 | 磁矩 |
|:---:|:---:|
| 14 | $\left(0,\;0,\;1\right)$ |
| 15 | $\left(0,\;0,\;-1\right)$ |

$$
\mathbf{M}_{\mathrm{net}}=\begin{pmatrix}0 \\ 0 \\ 0\end{pmatrix}
$$

共线：是；补偿：是；SOC：否。

异号自旋原子对：1 对。
位点映射：14→15 (Nb)。
连接操作：2 条。
交替磁初步判定：**初步对称性条件兼容交替磁候选**。
amcheck：`{"status":"ok","candidate_altermagnet":true}`。

动量空间对称约束：2 条。
$\mathbf{k}$ 使用倒易晶格分数坐标；$R_k=R^{-T}$。

**约束 #1**：$\bar{4}$（$S_{4}$）。

$$
R_{k,1}=\begin{pmatrix}0 & 1 & 0 \\ -1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix}
$$

**约束 #2**：$\bar{4}$（$S_{4}$）。

$$
R_{k,2}=\begin{pmatrix}0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & -1\end{pmatrix}
$$

$$
E_{\uparrow}(\mathbf{k})=E_{\downarrow}(R_{k,i}\mathbf{k}),\qquad \Delta(\mathbf{k})=-\Delta(R_{k,i}\mathbf{k})
$$

$i$ 为上列约束序号。


### 容差与后端

容差：`{"symprec_angstrom":0.001,"mag_symprec_mu_B":0.001,"findspingroup_eigenvalue_tol":2e-05,"findspingroup_matrix_tol":0.01}`。
FindSpinGroup 内部容差：`{"space_tol":0.001,"mtol":0.001,"meigtol":2e-05,"matrix_tol":0.01}`。
后端版本：`{"materials_symmetry":"0.3.0","spglib":"2.7.0","spinspg":"0.3.2","findspingroup":"0.15.17","amcheck":"1.0.2"}`。
警告：
- ComplexWarning: Casting complex values to real discards the imaginary part
