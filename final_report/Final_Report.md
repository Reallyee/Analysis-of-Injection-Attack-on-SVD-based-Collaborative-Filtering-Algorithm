## Anaylisis of Injection Attack on SVD-based Collaborative Filtering Algorithm



## Research Background 

Collaborative filtering(CF) algorithm is the most basic kind of algorithms in recommender system field. It is widely used in e-commerce, like Amazon. There are three kinds of collaborative filtering algorithms: user-based CF, item-based CF and model-based CF. In the second phase of the project, we have implemented a user-based CF recommender system and a SVD-based CF recommender system which is a kind of model-based CF recommender system. 

In the e-commerce competition, some intentional users inject a large number of falsified data in order to safeguard their own interests. Under such disturbances, the accuracy of recommender system decreases. Therefore, it is important to do research on the attack behavior of collaborative filtering recommender systems. Thus the research of Lam$^{[1]}$ got a result that item-based CF algorithm is more robust than user-based CF algorithm, the focus of our work is on attack behaviors to the SVD-based recommender system. We hack the system with random attack, mean attack and love/hate attack, then analize their effects on the SVD-based recommender system.



### SVD-based Collaborative Filtering Algorithm

毛毛把上一次的改一改放这里

### Injection Attacks

*Injection attack* indicates that attackers make the recommendation results biased through injecting falsified users into recommender systems. A *User Profile* is an n-dimendion vector $UP_i = (r_1,r_2,r_3,...,r_n)$ where *n* is the number of all items in the system. Denote $I$ as the item set of a recommender system and $I = I_T \cup I_S \cup I_F \cup I_{\emptyset}$ where $I_T$ is target items, $I_S$ is a set of items specified to improve the efficiency of the attack, $I_F$ is the set of items that need to be assigned a rating and $I_{\emptyset}$ is an unrated set of items. Hence, $Attack = (UP_1, UP_2, UP_3, ... , UP_{m-1})$.

There are four types of injection attack: basic attack, low-acknowledge attack, nuke attack and informed attack$^{[2]}$.

##### Basic attack

- Random attack

  Random attack is to select the user data of a certain fill size after the attacker determines the attack target, then scores the highest score or lowest score for the target items and scores the items in the $I_F$ randomly within a small range centered on the average value of all users for all the items. The average rating of all items by all users in many systems is public and the attacker can get this information, so the cost of knowledge for random attacks is minimal and realistically feasible.

- Mean attack

  The mean attack is basically the same as the random attack. The  difference is that the evaluation value of the item $i$ in the $I_F$ set is randomly selected within a very small range centered on the average evaluation value of the item $i$ by all the users. Its knowledge cost is high. It needs to know the average of all projects and it is difficult to achieve.

##### Low-acknowledge attack

- Bandwagon attack

  Bandwagon attack binds the target items with a small amount of popular items which have a large number of user groups. Therefore, the target items is more likely to be recommended.

- Segment attack

  Segment attack recommends target items to specific user groups. Attackers often bind the target items with the popular items that these users like. Therefore, the recommendation algorithm can easily recommend the target product to these user groups.

##### Nuke attack

- Love/hate attack

  It simply gives the highest score for those target items and the lowest score for those products that need to be filtered. This attack requires a very little bit of information, but it is very effective for user-based collaborative filtering algorithms.

- Reverse Bandwagon attack

  It is a variation of the Bandwagon attack. Unlike the Bandwagon attack, those target items are often tied to very unpopular items in the system. In this case, the system cannot easily recommend those target items.

##### Informed attack

- Popular attack

  It is for user-based CF algorithm. It needs more information, including the recommendation algorithm, the average score of the product, and the user's average score, because the similarities of users do not depend on the co-rated item number in practice and the Pearson correlation coefficient may be negative.Popular attack uses the average score of all items. According to whether the item's score is higher than the average, the item is rated $r_{min+1}$ and $r_{min}$, where $r_{min}$ represents the lowest score. Then, the Pearson correlation coefficient of falsified users and original users has a big probability to be positive, which means the predicted scores of target items are likely to be higher.

- Probe Attack Strategy

  Probe attack strategy is harder to detect than popular attack. It fakes a user first, then the system will recommend some items for it. With this recommendation information, we have some knowledge about its neighbors. Then we can attack the neighbors with other attack methods.

### Evaluation

把评估用到的方法、指标放这里

#### 结果和分析

。。。

### References

 [1] Lam S, Reidl J.Shiling recommender systems for fun and profit[C]//Proceedings of the 13th International WWW Conference, New York, 2002. 

[2] http://www.199it.com/archives/44483.html