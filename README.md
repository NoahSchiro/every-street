# Every Street

**DISCLAIMER**: This repository is still a work in progress

This repository is a part of a project to ride a bicycle on every street of Selinsgrove, PA, my home town. Selinsgrove is a small town, with only 6,000 people and less than 5 square kilometers of land. I believe it is possible to cover every street within the span of 1 day (and hopefully a lot less than that). In order to meet this time requirement though, we will want to compute the _provably_ shortest path we can take which will cover the length of each street once. In computer science, this problem is known as the [route inspection problem](https://en.wikipedia.org/wiki/Chinese_postman_problem).

If we model every street and intersection as edges and nodes within a graph, then we can run this algorithm and it will generate a route which is the shortest possible path that covers each street at least once. In order to do this, we will need to collect data on the town in question.