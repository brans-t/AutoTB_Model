# Theory and conventions

An ordinary operation is written `{R | t}` and acts on fractional direct coordinates as
`x' = R x + t`. It describes the nonmagnetic crystal. The crystallographic integer
matrix is converted through the lattice before Cartesian axes are inferred.

A magnetic operation is `{R | t}` with an optional time reversal. Magnetic moments are
axial vectors, so an unprimed spatial operation acts through `det(Q) Q` in Cartesian
coordinates, where `Q` is the Cartesian form of `R`; time reversal adds a minus sign.
The magnetic space group is therefore stored separately from the ordinary space group.

A spin-space operation is `[S || {R | t}]`. Here `S` acts on the Cartesian magnetic
moment and need not equal the spin action induced by `R`. The spinspg adapter returns
all three components. For every operation the analysis computes the site permutation,
checks species identity and periodic distance, and records whether an up site maps to a
down site. A matching `S` can then be tested against the ordered-moment direction.

FindSpinGroup independently standardizes this operation set and identifies its oriented
spin-space group (OSSG) index and symbol. The reported OSSG describes the nonrelativistic
spin-space symmetry. Its associated BNS magnetic group describes the SOC-compatible
case in which spin and real-space transformations are locked. Every identifier remains
paired with the backend's numerical tolerances and setting information.

For `x' = R x + t`, invariance of `k.x` gives the action on fractional reciprocal
coordinates `k' = R^-T k`. When an operation exchanges opposite-spin sectors, the
reported constraint is

```text
E_up(k) = E_down(R_k k)
Delta(k) = -Delta(R_k k)
```

where `Delta(k) = E_up(k) - E_down(k)`. This relation alone does not derive a d-wave,
g-wave, or other polynomial form.

The preliminary classifier first checks collinearity and compensation, then asks whether
opposite-spin sites are related by a pure translation, inversion, rotation, mirror, or
rotoinversion. Passing it yields “symmetry-compatible altermagnetic candidate.” A
complete proof of a particular momentum-dependent spin splitting requires the relevant
electronic states and representations. Relativistic SOC-driven splitting is a distinct
question and is not established by this nonrelativistic check.
