# Philosophy

## Perception

One of the essential problems with unsupervised machine learning is that,
despite what it might appear, there are an infinite number of ways to perceive
the world, and none need be canonical. If you want to perceive the world,
you first need to define some goal which the categorisation scheme can be allowed
to maximise. In this particular repository, the goal was to maximise the
expectation of the data given that we assume the data is made up of `K` Gaussians.


That this goal is analogous to our attempts to divide up the Southern Ocean is
not obvious. In some sense, it might be easier to justify a categorisation of
the ocean if its purpose was to predict some obvious physical variable, i.e.
`supervised learning`, which provides either a clear cost function to optimise,
or a series of similar cost functions that could be maximised.

## Possible objectives

The fronts of the Southern Ocean could correspond to:

  (a) The boundary between different water masses in the Southern Ocean.

  * where bondaries are distinct masses of water with distinct histories.

  * and there are a small and unambiguous number, `K`, of regions of water.

   _*or*_ 

  (b) The regions at which properties change suddenly, which could correspond 
      to those points at which the thermal wind balance leads to a jet.

  * A large gradient in density.

  * A large gradient in potential vorticity.

   _*or*_

  (c) The regions where there is a great deal of mixing upwards, and therefore there is 
      a greater ammount of biological productivity, leading to a source of food for the 
      Southern Ocean ecosystem.

  _*or*_

  (d) The divisions between different distinct ecological communities.


(a) and (d), (b) and (c) are quite closely related.
