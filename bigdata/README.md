## 作业一<3月19日>
### PageRank
- 算法实现
    - [PageRank算法简介及Map-Reduce实现](http://blog.jobbole.com/71431/)
    - [使用MapReduce实现PageRank算法](http://blog.csdn.net/u011955252/article/details/50535294)

- ECharts实现效果
    - 网页最初的关系图
     ![网页节点](http://7xoujr.com1.z0.glb.clouddn.com/begin.PNG)
    - 网页排序后
     ![网页节点](http://7xoujr.com1.z0.glb.clouddn.com/end.PNG)
    - Echarts图表实现[Demo](http://echarts.baidu.com/examples/editor.html?c=graph-simple&theme=light)
    
   通过改变Graph中各节点的属性值(参考[文档](http://echarts.baidu.com/option.html#series-graph.data))，如：
   ```
    data: [{
        name: '1',
        x: 10,
        y: 10,
        value: 10
    }, {
        name: '2',
        x: 100,
        y: 100,
        value: 20,
        symbolSize: 20,
        itemStyle: {
            color: 'red'
        }
    }]
    ```
### K-means
    - [基于MapReduce的k-means的并行化实现](http://blog.csdn.net/zhanghaodx082/article/details/21336437)
    - [基于MapReduce的并行k-means聚类](http://blog.csdn.net/baidu_35570545/article/details/72840734)
    - [K—Means聚类算法在MapReduce框架下的实现](http://www.fx361.com/page/2017/0121/621588.shtml)