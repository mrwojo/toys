A rough investigation of the Anscombe paradox and Ostrogorski paradox in majority votes on multiple issues. In a nutshell,

* Anscombe paradox: most voters can be in the minority on most issues
* Ostrogorski paradox: the tally of preferences per voter can contradict the tally of preferences per issue

These two counterintuitive results are similar yet not identical. This script illustrates situations in which they differ. It outputs textual descriptions representing different scenarios of voters and preferences on issues.

This was inspired by:

"[On the difference between the Anscombe and Ostrogorski paradoxes](http://economix.fr/fr/recrutement/2014/jpo-2014/papier_valeu.pdf)", Boniface Mbih and Aristide Valeu, 2014.

Output
======

```
Votes:
[[0 0 0]
 [0 0 0]
 [0 1 1]
 [0 1 1]
 [1 0 1]]
```

A voters × issues matrix: The 5 rows represent 5 voters. The 3 columns represent those voters' preferences on 3 issues (0 disapprove, 1 approve).

```
All preferences:     40.0%
```

40% of the above preferences are "approve" (6 ÷ 15).

```
Issue result:        False
Party result:        True
Ostrogorski paradox: True
O-Strict paradox:    False
```

Issue result: Most of the issues are disapproved of by most of the voters. The first issue is 1 vs. 4, the second is 2 vs. 3, the third is 3 vs. 2. If these 3 issues represent parts of a plan, and each part is voted on separately (each voter cast 3 votes, 1 for each issue), then the plan is rejected because most parts are rejected.

Party result: However, most of the voters approve of most of the issues. Again, if these 3 issues represented parts of a plan, but this time each of the 5 voters cast just 1 vote based on their overall opinion of the issues, then the plan is accepted because most voters are mostly satisfied.

The contradiction between the "issue result" and the "party result" is the Ostrogorski paradox.

This example does not represent a more strict version of the Ostrogorski paradox, which would mean that the issue result is unanimously opposed to the party result.

```
Voters' frustration:
[[0 0 1]
 [0 0 1]
 [0 1 0]
 [0 1 0]
 [1 0 0]]
Societal frustration [False False False False False]
Anscombe paradox:    False
```

The voters' frustration matrix is voters × "frustrated decision". 1 indicates the voter is in the minority for that issue. The first 2 voters are frustrated on the 3rd issue because they disapprove of it whereas most voters approve.

The "societal frustration" indicates whether the 5 voters are frustrated on most issues. None of the voters are mostly frustrated. (They all happen to be frustrated on only 1 of 3 issues.)

Finally, this lack of frustration indicates that there is no Anscombe paradox.

Strict Ostrogorski example
==========================

```
Votes:
[[0 0 1]
 [0 1 0]
 [1 0 0]
 [1 1 1]
 [1 1 1]]
```

Each of the 3 issues are supported by 3 of 5 voters but only 2 of 5 voters vote in favor.

The strict Ostrogorski examples I've found also exhibit the Anscombe paradox (but not necessarily vice versa).

Anscombe without Ostrogorski
============================

```
Votes:
[[0 0 0]
 [0 1 1]
 [1 0 1]
 [1 1 0]
 [1 1 0]]
Voters' frustration:
[[1 1 0]   <- mostly frustrated
 [1 0 1]   <- mostly frustrated
 [0 1 1]   <- mostly frustrated
 [0 0 0]
 [0 0 0]]
Societal frustration [ True  True  True False False]
```

The first 3 of 5 voters are frustrated on 2 of 3 issues. For instance, the first voter is in the minority on the first 2 issues.
