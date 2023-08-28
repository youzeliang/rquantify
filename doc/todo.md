

基于富途证券开放的futuAPI接口，对恒生指数牛熊进行日内高频炒单的程序交易系统，包含实时筛选牛熊交易标的和交易策略两部分。交易策略有三块：入场，止盈和止损。入场和止损的信号主要来源于一分钟K线突破前一分钟k线的最高价和最低价，同时用收盘价、10均线和20均线组成的均线系统进行了过滤。止盈部分主要是卖二卖一排队卖，改单信号来源于当前一分钟k线的最高价、最低价和收盘价与5均线的比较。



一、牛熊筛选

    warrant_pool1      选出恒指的牛熊，发行商为法巴、摩通、法兴

    warrant_pool2(bear_pool1, bull_pool1) 筛选换股比率为10000、街货比小于50%的恒指牛熊、最新价格小于0.180, 记录下它们的收回价

    update_warrant_pool(bear_pool2, bear_rec_price, bull_pool2, bull_rec_price) 实时更新牛熊池, 恒指当月期货价格距离熊收回价小于-0.75%，距离牛收回价大于0.75%


二、入场

    avg_state_rank(data)          根据收盘价和一分钟10,20日均线值的大小，来评价走势的强弱，对信号进行过滤分类

    set_buy_trigger_range(data)   设置买牛熊触发值的范围(入场)

    buy_trigger_signal(data)      设置触发买牛熊的信号（入场）

    market_in(data, bear_candidate_list, bull_candidate_list)  当信号出现时，以买一价或者中间价排队买入

    chase_buy_change_order(data)  当排队买入未全部成交且往盈利方向变化超4格且小于10格时，立马以卖一价或者中间价买入


三、止盈

    compare_with_avg_line5(data)  每一根一分钟k线的最低价、最高价和中间价与一分钟k线的5日均线比较，用来评估近几分钟走势的强弱（止盈，排队卖）

    market_out(data)              包括止盈和止损两部分



四、止损

    avg_state_rank(data)          根据收盘价和一分钟10,20日均线值的大小，来评价走势的强弱，对信号进行过滤分类

    set_sell_trigger_range(data)  设置卖牛熊触发值的范围(止损)

    sell_trigger_signal(data)     设置触发卖牛熊的信号（止损）

    market_out(data)              包括止盈和止损两部分

    chase_sell_change_order(data)  当止损未全部成交且往亏损方向变化超5格时，立马以买一价格卖出
