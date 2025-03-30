import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
import os
import json
from datetime import datetime, timedelta
import random

# 确保目录存在
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)

# 初始化会话状态
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 1. 全局配置
st.set_page_config(
    page_title="绿链智田 - 低碳智慧供应链赋能乡村振兴平台", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': '绿链智田 - 低碳智慧供应链赋能乡村振兴平台 v1.0'
    }
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #388E3C;
        margin-bottom: 0.8rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #F1F8E9;
        margin-bottom: 1rem;
    }
    .highlight {
        color: #1B5E20;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #757575;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    .success-msg {
        padding: 1rem;
        background-color: #C8E6C9;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .info-msg {
        padding: 1rem;
        background-color: #BBDEFB;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 2. 侧边栏导航与登录
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>绿链智田</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>低碳智慧供应链赋能乡村</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 用户登录系统
    if not st.session_state.user_logged_in:
        st.subheader("用户登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("登录"):
            # 读取用户数据
            with open("data/users.json", "r", encoding="utf-8") as f:
                users_data = json.load(f)
            
            # 验证用户信息
            user_found = False
            for user in users_data["users"]:
                if user["username"] == username and user["password"] == password:
                    user_found = True
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = user["role"]
                    st.success(f"欢迎回来，{username}！您的身份是：{user['role']}")
                    st.rerun()
                    break
            
            if not user_found:
                st.error("用户名或密码错误！")
                st.info("提示：可以使用以下任一账户登录：\n- 管理员：admin/admin123\n- 农户：farmer1/farm2025\n- 消费者：customer1/cust2025\n- 商家：business1/busi2025\n- 游客：guest/guest123")
    else:
        st.success(f"已登录: {st.session_state.username}")
        if st.button("退出登录"):
            st.session_state.user_logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    st.markdown("---")
    
    # 导航菜单
    st.subheader("功能导航")
    page = st.radio("", [
        "首页",
        "农产品自营商城",
        "农产家庭直供",
        "营养定期送服务",
        "共享农庄模块",
        "会员民宿模块",
        "乡村亲子模块",
        "购物车"
    ])
    
    # 显示购物车数量
    if st.session_state.cart:
        st.info(f"购物车: {len(st.session_state.cart)} 件商品")
    
    st.markdown("---")
    st.markdown("### 技术支持")
    st.markdown("- ✅ 区块链溯源")
    st.markdown("- ✅ AIoT智能监测")
    st.markdown("- ✅ RFID物流跟踪")
    st.markdown("- ✅ 大数据分析")
    
    st.markdown("---")
    st.markdown("<div class='footer'>© 2025 绿链智田 版权所有</div>", unsafe_allow_html=True)

# 3. 模拟数据准备
# 商品数据
@st.cache_data
def load_products():
    products = {
        "有机大米": {
            "price": 20, 
            "origin": "河北农场", 
            "trace_id": "XM12345", 
            "stock": 100,
            "description": "纯天然有机种植，无农药残留，口感醇厚",
            "image": "images/有机大米.png",
            "carbon": 0.5,
            "category": "粮油"
        },
        "茶叶": {
            "price": 35,
            "origin": "福建农场",
            "trace_id": "CY13579",
            "stock": 120,
            "description": "高山云雾茶，清香醇厚，回甘持久",
            "image": "images/茶叶.png",
            "carbon": 0.2,
            "category": "饮品"
        },
        "面粉": {
            "price": 18,
            "origin": "河南农场",
            "trace_id": "MF24680",
            "stock": 150,
            "description": "优质小麦研磨，细腻柔滑，适合烘焙",
            "image": "images/面粉.png",
            "carbon": 0.3,
            "category": "粮油"
        },
        "食用油": {
            "price": 45,
            "origin": "山东农场",
            "trace_id": "SY35791",
            "stock": 100,
            "description": "物理压榨，零添加，健康食用",
            "image": "images/食用油.png",
            "carbon": 0.4,
            "category": "粮油"
        },
        "低碳苹果": {
            "price": 15, 
            "origin": "山东农场", 
            "trace_id": "AP67890", 
            "stock": 150,
            "description": "低碳种植技术，减少30%碳排放，果肉脆甜",
            "image": "images/苹果.png",
            "carbon": 0.3,
            "category": "水果"
        },
        "生态蜂蜜": {
            "price": 50, 
            "origin": "云南农场", 
            "trace_id": "HM54321", 
            "stock": 80,
            "description": "高山野生蜂蜜，纯天然无添加，营养丰富",
            "image": "images/生态蜂蜜.png",
            "carbon": 0.2,
            "category": "调味品"
        },
        "有机菠菜": {
            "price": 8, 
            "origin": "江苏农场", 
            "trace_id": "BS78901", 
            "stock": 200,
            "description": "富含铁质和维生素，有机种植，新鲜采摘",
            "image": "images/菠菜.png",
            "carbon": 0.1,
            "category": "蔬菜"
        },
        "土鸡蛋": {
            "price": 25, 
            "origin": "安徽农场", 
            "trace_id": "JD24680", 
            "stock": 120,
            "description": "散养土鸡产蛋，蛋黄色泽金黄，营养丰富",
            "image": "images/鸡蛋.png",
            "carbon": 0.4,
            "category": "禽蛋"
        }
    }
    return products

# 生鲜直供数据
@st.cache_data
def load_fresh_items():
    fresh_items = {
        "生态西红柿": {
            "price": 15, 
            "origin": "河北农场", 
            "delivery_time": 6,
            "image": "https://img.zcool.cn/community/01f9c55d31a173a8012187f4c1f5ba.jpg@1280w_1l_2o_100sh.jpg"
        },
        "新鲜土豆": {
            "price": 10, 
            "origin": "甘肃农场", 
            "delivery_time": 8,
            "image": "https://img.zcool.cn/community/01a4a85af3c3c9a801219741cd7b8b.jpg@1280w_1l_2o_100sh.jpg"
        },
        "有机白菜": {
            "price": 8, 
            "origin": "山东农场", 
            "delivery_time": 5,
            "image": "https://img.zcool.cn/community/01c2ce5d0e9f8aa801219c7748b2b9.jpg@1280w_1l_2o_100sh.jpg"
        },
        "山区胡萝卜": {
            "price": 12, 
            "origin": "陕西农场", 
            "delivery_time": 7,
            "image": "https://img.zcool.cn/community/01d0f05af3c3c9a801219741f6c3a0.jpg@1280w_1l_2o_100sh.jpg"
        }
    }
    return fresh_items

# 农场监测数据（模拟）
@st.cache_data
def generate_farm_data():
    now = datetime.now()
    dates = [now - timedelta(hours=i) for i in range(24)]
    dates.reverse()
    
    # 生成更真实的温度数据（白天高，晚上低）
    temperatures = []
    for date in dates:
        hour = date.hour
        # 模拟日夜温差
        if 6 <= hour <= 18:  # 白天
            base_temp = 25 + 5 * np.sin(np.pi * (hour - 6) / 12)
        else:  # 晚上
            if hour < 6:
                base_temp = 20 - 5 * np.sin(np.pi * hour / 12)
            else:
                base_temp = 20 - 5 * np.sin(np.pi * (hour - 18) / 6)
        
        # 添加随机波动
        temp = base_temp + np.random.uniform(-1, 1)
        temperatures.append(temp)
    
    # 湿度与温度有一定反相关
    humidity = [max(min(100 - temp + np.random.uniform(40, 50), 95), 40) for temp in temperatures]
    
    # 光照强度（白天高，晚上低）
    light = []
    for date in dates:
        hour = date.hour
        if 6 <= hour <= 18:  # 白天
            base_light = 800 * np.sin(np.pi * (hour - 6) / 12)
            light_value = base_light + np.random.uniform(-50, 50)
        else:  # 晚上
            light_value = np.random.uniform(0, 10)
        light.append(max(0, light_value))
    
    # 土壤湿度（较为稳定，有小幅波动）
    soil_moisture = [60 + np.random.uniform(-5, 5) for _ in range(24)]
    
    farm_data = pd.DataFrame({
        "时间": dates,
        "温度(°C)": temperatures,
        "湿度(%)": humidity,
        "光照(lux)": light,
        "土壤湿度(%)": soil_moisture
    })
    
    return farm_data

# 加载数据
products = load_products()
fresh_items = load_fresh_items()
farm_data = generate_farm_data()

# 4. 功能模块实现
# 4.0 首页
# 3. 主页内容
if page == "首页":
    st.markdown("<h1 class='main-header'>绿链智田 - 低碳智慧供应链赋能乡村振兴平台</h1>", unsafe_allow_html=True)
    
    # # 显示首页图片
    # st.image("images/首页.png", use_container_width=True, width=600)
    
    # 平台介绍
    st.markdown("""
    <div class='card'>
        <h2 class='sub-header'>平台简介</h2>
        <p>"绿链智田"是一个致力于连接城乡供需、推动农业现代化的数字农业服务平台。我们以"从源头解决亚健康，构建健康生活新生态"为使命，整合优质农产品资源，提供从田间到餐桌的全链条服务。平台涵盖线上农产品商城、家庭直供、营养定制，以及线下共享农庄、民宿和亲子体验等多种业务，满足城市居民对安全、新鲜食材和田园生活的需求，同时为乡村经济发展注入新活力。通过高效的供应链和创新的服务模式，"绿链智田"打造了一个可持续的农业生态圈，助力城乡融合与乡村振兴。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 图片位置预留
    # st.image("images/farm.svg", caption="河北农场实景（示例）")
    
    # 平台特色
    st.markdown("""
    <div class='card'>
        <h2 class='sub-header'>平台特色</h2>
        <ul>
            <li><span class='highlight'>全链条生态服务：</span>"绿链智田"无缝连接农产品生产、销售与体验，提供线上购买、线下采摘的一站式服务。用户既能在家中享用新鲜食材，也能带家人走进田园，体验种植与度假的乐趣，真正实现城乡生活的双向互动。</li>
            <li><span class='highlight'>品质与新鲜兼得：</span>平台精选全国优质农场资源，确保食材从采摘到送达的高效流通。家庭直供实现半日达配送，营养定期送满足个性化健康需求，让每一餐都成为安心与美味的享受。</li>
            <li><span class='highlight'>政策赋能，振兴乡村先行：</span>紧跟国家2025年"中央1号文件"关于农村产业升级与乡村融合的政策，"绿链智田"积极响应政策号召，利用农村电商扶持和冷链物流下沉的支持，赋能乡村生产者增收，年带动就业1万人，推动农业现代化与地方经济发展。</li>
            <li><span class='highlight'>多元化用户体验：</span>通过共享农庄、民宿和亲子活动，平台为城市家庭提供多样化的田园生活方式。会员制设计让用户以低成本畅享全年服务，年票模式提升参与感受，重新定义健康与休闲的结合。</li>
            <li><span class='highlight'>绿色发展引领：</span>平台践行国家绿色低碳政策，推广可持续农业模式，年为乡村增收的同时，推动生态保护与经济效益的双赢，为"2060碳中和"目标贡献力量。</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 技术特色
    st.markdown("<h2 class='sub-header'>技术特色</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='card'>
            <h3>区块链溯源</h3>
            <p>运用区块链技术，实现农产品从种植、采收、加工到销售的全程可追溯，确保食品安全。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3>AIoT智能监测</h3>
            <p>通过物联网传感器实时监测农田环境数据，AI算法分析生长状况，提供智能种植建议。</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card'>
            <h3>RFID物流跟踪</h3>
            <p>RFID技术实现物流全程跟踪，优化配送路径，提高物流效率，降低损耗。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h3>大数据分析</h3>
            <p>基于用户消费习惯和市场需求的大数据分析，为农户提供精准种植建议，实现产销平衡。</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 数据展示
    st.markdown("<h2 class='sub-header'>平台数据</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("服务农户", "10,000+", "+15%")
    
    with col2:
        st.metric("合作基地", "100+", "+8%")
    
    with col3:
        st.metric("产品品类", "500+", "+20%")
    
    with col4:
        st.metric("年交易额", "¥5000万", "+25%")

# 4.1 农产品自营商城
elif page == "农产品自营商城":
    st.markdown("<h1 class='main-header'>农产品自营商城</h1>", unsafe_allow_html=True)
    st.markdown("<p>浏览高品质农特产品，区块链溯源确保安全透明。</p>", unsafe_allow_html=True)
    
    # 商品筛选
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "商品分类", 
            ["全部"] + list(set(product["category"] for product in products.values()))
        )
    
    with col2:
        price_range = st.slider("价格范围", 0, 100, (0, 100))
    
    with col3:
        sort_by = st.selectbox("排序方式", ["价格从低到高", "价格从高到低", "碳足迹从低到高"])
    
    # 筛选和排序商品
    filtered_products = {}
    for name, info in products.items():
        if (category_filter == "全部" or info["category"] == category_filter) and \
           (price_range[0] <= info["price"] <= price_range[1]):
            filtered_products[name] = info
    
    # 排序
    if sort_by == "价格从低到高":
        sorted_products = dict(sorted(filtered_products.items(), key=lambda item: item[1]["price"]))
    elif sort_by == "价格从高到低":
        sorted_products = dict(sorted(filtered_products.items(), key=lambda item: item[1]["price"], reverse=True))
    else:  # 碳足迹从低到高
        sorted_products = dict(sorted(filtered_products.items(), key=lambda item: item[1]["carbon"]))
    
    # 商品展示
    if not sorted_products:
        st.warning("没有符合条件的商品")
    else:
        # 每行显示3个商品
        for i in range(0, len(sorted_products), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(sorted_products):
                    product_name = list(sorted_products.keys())[i + j]
                    product_info = sorted_products[product_name]
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class='card'>
                            <h3>{product_name}</h3>
                            <p>价格：¥{product_info['price']}</p>
                            <p>产地：{product_info['origin']}</p>
                            <p>碳足迹：{product_info['carbon']}kg</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.image(product_info["image"], use_container_width=True, width=300)
                        st.write(product_info["description"])
                        
                        # 区块链溯源查询
                        if st.button(f"查询溯源信息 #{product_name}", key=f"trace_{product_name}"):
                            with st.spinner("正在查询区块链数据..."):
                                time.sleep(1)  # 模拟查询延迟
                                st.success(f"""
                                溯源结果：{product_name}
                                - 种植日期：2025-01-15
                                - 采摘日期：2025-03-10
                                - 检测结果：无农药残留
                                - 碳足迹：{product_info['carbon']}kg
                                - 区块高度：#7654321
                                - 交易哈希：0x8f7e6d5c4b3a2910...
                                """)
                        
                        # 加入购物车
                        quantity = st.number_input(
                            "购买数量", 
                            min_value=1, 
                            max_value=product_info["stock"], 
                            value=1,
                            key=f"qty_{product_name}"
                        )
                        
                        if st.button(f"加入购物车 #{product_name}", key=f"add_{product_name}"):
                            st.session_state.cart.append({
                                "name": product_name,
                                "price": product_info["price"],
                                "quantity": quantity,
                                "total": product_info["price"] * quantity
                            })
                            st.success(f"{product_name} x {quantity} 已加入购物车！")

# 4.2 农产家庭直供
elif page == "农产家庭直供":
    st.markdown("<h1 class='main-header'>农产家庭直供</h1>", unsafe_allow_html=True)
    st.markdown("<p>从农场直达家庭，新鲜生鲜半日达。</p>", unsafe_allow_html=True)
    
    # 生鲜展示
    st.markdown("<h2 class='sub-header'>今日鲜选</h2>", unsafe_allow_html=True)
    
    # 商品网格布局
    cols = st.columns(3)
    fresh_items_list = [
        {"name": "生态西红柿", "price": 8, "origin": "河北农场", "delivery_time": 6, "image": "images/西红柿.png"},
        {"name": "有机白菜", "price": 6, "origin": "山东农场", "delivery_time": 5, "image": "images/白菜.png"},
        {"name": "新鲜土豆", "price": 5, "origin": "甘肃农场", "delivery_time": 8, "image": "images/土豆.png"},
        {"name": "紫皮茄子", "price": 7, "origin": "河南农场", "delivery_time": 6, "image": "images/茄子.png"},
        {"name": "山区胡萝卜", "price": 4, "origin": "陕西农场", "delivery_time": 7, "image": "images/胡萝卜.png"},
        {"name": "新鲜辣椒", "price": 6, "origin": "四川农场", "delivery_time": 6, "image": "images/辣椒.png"}
    ]
    
    for i, item in enumerate(fresh_items_list):
        with cols[i % 3]:
            st.image(item["image"], caption=item["name"], use_container_width=True)
            st.markdown(f"""
            <div class='card'>
                <p>价格：¥{item['price']}/斤</p>
                <p>产地：{item['origin']}</p>
                <p>预计配送时间：{item['delivery_time']}小时内</p>
            </div>
            """, unsafe_allow_html=True)
            
            quantity = st.number_input(f"数量（斤）", min_value=1, value=1, key=f"qty_{item['name']}")
            total_price = item["price"] * quantity
            st.write(f"总价：¥{total_price}")
            
            if st.button(f"选择购买", key=f"buy_{item['name']}"):
                st.session_state.selected_item = item
                st.session_state.selected_quantity = quantity
                st.session_state.selected_total = total_price
    
    # 配送信息和订单追踪并排显示
    st.markdown("<h2 class='sub-header'>配送信息与订单追踪</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("配送信息")
        address = st.text_input("配送地址")
        phone = st.text_input("联系电话")
        
        if 'selected_item' in st.session_state and st.button("立即下单"):
            if address and phone:
                with st.spinner("正在处理订单..."):
                    time.sleep(1)
                    st.session_state.orders.append({
                        "item": st.session_state.selected_item["name"],
                        "quantity": st.session_state.selected_quantity,
                        "total": st.session_state.selected_total,
                        "address": address,
                        "phone": phone,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "已下单"
                    })
                    st.success(f"已下单：{st.session_state.selected_item['name']} {st.session_state.selected_quantity}斤，预计{st.session_state.selected_item['delivery_time']}小时送达！")
            else:
                st.error("请填写完整的配送信息")
    
    with col2:
        st.subheader("订单追踪")
        
        if st.session_state.orders:
            order_to_track = st.selectbox(
                "选择订单", 
                [f"{order['item']} - {order['time']}" for order in st.session_state.orders]
            )
            
            selected_order_idx = [f"{order['item']} - {order['time']}" for order in st.session_state.orders].index(order_to_track)
            selected_order = st.session_state.orders[selected_order_idx]
            
            # 物流跟踪（RFID模拟）
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("订单状态")
            st.write(f"商品：{selected_order['item']} x {selected_order['quantity']}斤")
            st.write(f"下单时间：{selected_order['time']}")
            
            # 模拟物流状态
            with st.spinner("正在查询物流信息..."):
                time.sleep(1)
                
                # 根据下单时间计算当前物流状态
                order_time = datetime.strptime(selected_order['time'], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                hours_passed = (now - order_time).total_seconds() / 3600
                
                # 物流状态进度条
                if hours_passed < 1:
                    progress = 0.2
                    status = "订单已确认，正在准备"
                elif hours_passed < 2:
                    progress = 0.4
                    status = "农场采摘完成"
                elif hours_passed < 3:
                    progress = 0.6
                    status = "RFID分拣完成，正在配送中"
                elif hours_passed < 4:
                    progress = 0.8
                    status = "已到达配送站点，即将送达"
                else:
                    progress = 1.0
                    status = "已送达"
                
                st.progress(progress)
                st.write(f"当前状态：{status}")
                
                # 物流详情
                st.write("物流详情：")
                if hours_passed >= 0:
                    st.write(f"- {order_time.strftime('%H:%M:%S')} 订单已确认，正在准备")
                if hours_passed >= 1:
                    st.write(f"- {(order_time + timedelta(hours=1)).strftime('%H:%M:%S')} 农场采摘完成")
                if hours_passed >= 2:
                    st.write(f"- {(order_time + timedelta(hours=2)).strftime('%H:%M:%S')} RFID分拣完成，正在配送中")
                if hours_passed >= 3:
                    st.write(f"- {(order_time + timedelta(hours=3)).strftime('%H:%M:%S')} 已到达配送站点，即将送达")
                if hours_passed >= 4:
                    st.write(f"- {(order_time + timedelta(hours=4)).strftime('%H:%M:%S')} 已送达")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # RFID技术说明
            st.markdown("""
            <div class='info-msg'>
                <h4>RFID智能物流</h4>
                <p>我们采用RFID技术对农产品进行全程跟踪，实现从农场到餐桌的全链路可视化。
                RFID标签记录了产品的采摘时间、分拣时间、运输路径等信息，确保产品新鲜度和可追溯性。</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("暂无订单记录，请先下单")

# 4.3 营养定期送服务
elif page == "营养定期送服务":
    st.markdown("<h1 class='main-header'>营养定期送服务</h1>", unsafe_allow_html=True)
    st.markdown("<p>AI定制健康食谱，定期配送到家。</p>", unsafe_allow_html=True)
    
    # 添加CSS样式使右侧订阅服务固定
    st.markdown("""
    <style>
    .subscription-container {
        position: fixed;
        right: 2rem;
        top: 8rem;
        width: 25%;
        max-height: 85vh;
        overflow-y: auto;
        padding-right: 1rem;
        z-index: 1000;
    }
    .main-content {
        width: 70%;
        padding-right: 28%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 主内容区域
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>个性化营养方案</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # 用户信息输入
    st.subheader("输入健康信息")
    age = st.slider("年龄", 1, 100, 30)
    gender = st.selectbox("性别", ["男", "女"])
    health_goals = st.multiselect("健康目标", ["减重", "增肌", "控糖", "降压", "提高免疫力的", "儿童成长"])
    dietary_restrictions = st.multiselect("饮食限制", ["无", "素食", "无麸质", "低盐", "低糖"])
    
    # 生成个性化食谱
    if st.button("生成个性化食谱"):
        with st.spinner("AI正在分析您的健康数据..."):
            time.sleep(2)  # 模拟AI处理时间
            
            # 根据用户选择生成食谱推荐
            st.subheader("您的个性化食谱")
            
            # 根据健康目标和饮食限制生成食谱
            if "降压" in health_goals or "低盐" in dietary_restrictions:
                breakfast = "全麦面包配低脂奶酪 + 蓝莓"
                lunch = "低盐蒸鱼 + 西兰花 + 糙米饭"
                dinner = "菠菜豆腐汤 + 紫薯"
            elif "控糖" in health_goals or "低糖" in dietary_restrictions:
                breakfast = "燕麦粥 + 坚果"
                lunch = "鸡胸肉沙拉 + 藜麦"
                dinner = "清蒸鲈鱼 + 芦笋 + 小份糙米"
            elif "儿童成长" in health_goals:
                breakfast = "鸡蛋牛奶燕麦粥 + 草莓"
                lunch = "番茄肉酱意面 + 牛奶"
                dinner = "胡萝卜排骨汤 + 蔬菜饭团"
            elif "增肌" in health_goals:
                breakfast = "高蛋白奶昔 + 全麦吐司 + 香蕉"
                lunch = "烤鸡胸肉 + 红薯 + 西兰花"
                dinner = "三文鱼 + 藜麦 + 什锦蔬菜"
            else:
                breakfast = "水果燕麦碗 + 酸奶"
                lunch = "时令蔬菜沙拉 + 糙米饭"
                dinner = "清炒时蔬 + 豆腐 + 小份糙米"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                **早餐**
                {breakfast}
                """)
            
            with col2:
                st.markdown(f"""
                **午餐**
                {lunch}
                """)
            
            with col3:
                st.markdown(f"""
                **晚餐**
                {dinner}
                """)
            
            # 营养分析
            st.subheader("营养分析")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("蛋白质", "65g", "+15%")
            with col2:
                st.metric("碳水化合物", "200g", "-10%")
            with col3:
                st.metric("脂肪", "50g", "-5%")
            with col4:
                st.metric("膳食纤维", "25g", "+30%")
            
            # 显示食材来源
            st.subheader("食材来源")
            st.write("所有食材均来自我们合作的有机农场，保证新鲜和安全。")
            
            # 显示大数据分析说明
            st.info("此食谱由AI基于10万+用户的健康数据和营养学研究生成，针对您的个人情况进行了优化。")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # 固定在右侧的订阅服务
    st.markdown("<div class='subscription-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>订阅服务</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
        
    # 订阅计划选择
    st.subheader("选择订阅计划")
    plan = st.radio("配送周期", ["每周配送", "每两周配送", "每月配送"])
    
    # 价格计算
    if plan == "每周配送":
        price = 298
        meals = 21
    elif plan == "每两周配送":
        price = 168
        meals = 10
    else:
        price = 98
        meals = 5
    
    st.write(f"价格: ¥{price}/期")
    st.write(f"包含: {meals}份餐食")
    
    # 配送地址
    st.subheader("配送信息")
    address = st.text_input("配送地址")
    phone = st.text_input("联系电话")
    
    # 支付方式
    payment = st.selectbox("支付方式", ["微信支付", "支付宝", "银行卡"])
    
    # 确认订阅
    if st.button("确认订阅"):
        if address and phone:
            with st.spinner("正在处理订阅请求..."):
                time.sleep(1)
                st.success(f"订阅成功！您已订阅{plan}营养套餐，首次配送将在3天内送达。")
                
                # 显示订阅详情
                st.subheader("订阅详情")
                st.write(f"订阅计划: {plan}")
                st.write(f"配送地址: {address}")
                st.write(f"联系电话: {phone}")
                st.write(f"支付方式: {payment}")
                st.write(f"订阅日期: {datetime.now().strftime('%Y-%m-%d')}")
                st.write(f"首次配送日期: {(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')}")
        else:
                st.error("请填写完整的配送信息")
        
        # 营养师支持
        st.markdown("""
        <div class='info-msg'>
            <h4>专业营养师支持</h4>
            <p>订阅用户可享受专业营养师一对一咨询服务，每月一次，帮助您调整饮食计划，实现健康目标。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# 4.4 共享农庄模块
elif page == "共享农庄模块":
    st.markdown("<h1 class='main-header'>共享农庄模块</h1>", unsafe_allow_html=True)
    st.markdown("<p>线上认种，线下采摘，体验田园生活。</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h2 class='sub-header'>认种地块</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 地块选择
        st.subheader("选择地块")
        # 显示农场照片
        farm_location = st.selectbox("农场位置", ["河北农场", "山东农场", "云南农场"])
        # 根据选择显示对应农场的照片
        farm_image_path = os.path.join("images", f"{farm_location}.png")
        if os.path.exists(farm_image_path):
            st.image(farm_image_path, caption=f"{farm_location}实景", use_container_width=True)
        plot_size = st.selectbox("地块面积", ["5平米", "10平米", "20平米"])
        
        # 作物选择
        st.subheader("选择作物")
        season = st.radio("种植季节", ["春季", "夏季", "秋季"])
        
        # 根据季节显示不同作物
        if season == "春季":
            crops = ["菠菜", "生菜", "胡萝卜", "草莓"]
        elif season == "夏季":
            crops = ["西红柿", "黄瓜", "茄子", "辣椒"]
        else:
            crops = ["白菜", "萝卜", "南瓜", "土豆"]
        
        crop = st.selectbox("种植作物", crops)
        
        # 计算价格
        if plot_size == "5平米":
            base_price = 500
        elif plot_size == "10平米":
            base_price = 900
        else:
            base_price = 1600
        
        # 显示价格和收益预估
        st.subheader("价格与收益")
        st.write(f"认种费用: ¥{base_price}/季")
        
        # 预估产量和价值
        if plot_size == "5平米":
            estimated_yield = "15-20kg"
            estimated_value = "¥300-400"
        elif plot_size == "10平米":
            estimated_yield = "30-40kg"
            estimated_value = "¥600-800"
        else:
            estimated_yield = "60-80kg"
            estimated_value = "¥1200-1600"
        
        st.write(f"预估产量: {estimated_yield}")
        st.write(f"预估价值: {estimated_value}")
        
        # 认种按钮
        if st.button("确认认种"):
            with st.spinner("正在处理认种请求..."):
                time.sleep(1)
                st.success(f"认种成功！您已认种{farm_location}的{plot_size}地块，种植{crop}，费用¥{base_price}。")
                st.info(f"种植周期：约90天，预计收获日期：{(datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h2 class='sub-header'>AIoT智能监测</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 选择查看的农场
        farm_to_monitor = st.selectbox("选择监测农场", ["河北农场", "山东农场", "云南农场"])
        
        # 显示实时数据
        st.subheader("实时环境数据")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_temp = farm_data["温度(°C)"].iloc[-1]
            st.metric("温度", f"{current_temp:.1f}°C", f"{current_temp - farm_data['温度(°C)'].iloc[-2]:.1f}°C")
        
        with col2:
            current_humidity = farm_data["湿度(%)"].iloc[-1]
            st.metric("湿度", f"{current_humidity:.1f}%", f"{current_humidity - farm_data['湿度(%)'].iloc[-2]:.1f}%")
        
        with col3:
            current_light = farm_data["光照(lux)"].iloc[-1]
            st.metric("光照", f"{current_light:.0f} lux", f"{current_light - farm_data['光照(lux)'].iloc[-2]:.0f}")
        
        with col4:
            current_soil = farm_data["土壤湿度(%)"].iloc[-1]
            st.metric("土壤湿度", f"{current_soil:.1f}%", f"{current_soil - farm_data['土壤湿度(%)'].iloc[-2]:.1f}%")
        
        # 环境数据图表
        st.subheader("24小时环境趋势")
        chart_data = farm_data.melt(id_vars=["时间"], value_vars=["温度(°C)", "湿度(%)", "土壤湿度(%)"])
        fig = px.line(chart_data, x="时间", y="value", color="variable", title="环境参数变化趋势")
        st.plotly_chart(fig, use_container_width=True)
        
        # 光照单独图表（因为数值范围差异大）
        light_fig = px.line(farm_data, x="时间", y="光照(lux)", title="光照强度变化")
        st.plotly_chart(light_fig, use_container_width=True)
        
        # 智能灌溉状态
        st.subheader("智能灌溉状态")
        if farm_data["土壤湿度(%)"].iloc[-1] < 55:
            st.warning("土壤湿度低，已启动智能灌溉系统")
            irrigation_status = "运行中"
        else:
            st.success("土壤湿度正常，智能灌溉系统待机")
            irrigation_status = "待机"
        
        st.write(f"灌溉系统状态: {irrigation_status}")
        st.write(f"上次灌溉时间: {(datetime.now() - timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M')}")
        
        # AIoT技术说明
        st.markdown("""
        <div class='info-msg'>
            <h4>AIoT智能监测系统</h4>
            <p>我们的AIoT系统通过物联网传感器实时监测农田环境，AI算法分析生长状况，自动控制灌溉、温室等设备，
            确保作物在最佳环境中生长。您可以随时通过手机APP查看您认种地块的实时状态。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # AR虚拟漫游
    st.markdown("<h2 class='sub-header'>AR虚拟漫游</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    st.write("通过AR技术，足不出户体验农场实景。")
    farm_to_view = st.selectbox("选择农场", ["河北农场", "山东农场", "云南农场"], key="ar_farm")
    
    # 显示农场实景图片
    col1, col2 = st.columns([2, 1])
    
    with col1:
        farm_image_path = os.path.join("images", f"{farm_to_view}.png")
        if os.path.exists(farm_image_path):
            st.image(farm_image_path, caption=f"{farm_to_view}实景", use_container_width=True)
        else:
            st.warning("农场实景图片暂未上传")
    
    with col2:
        st.subheader("AR导览")
        st.write("1. 扫描二维码，下载AR应用")
        st.write("2. 打开应用，选择农场")
        st.write("3. 对准平面，开始虚拟漫游")
        
        if st.button("模拟AR体验"):
            with st.spinner("正在加载AR体验..."):
                time.sleep(2)
                st.success("AR体验已就绪！")
                st.write("您可以看到：")
                st.write("- 作物生长状态")
                st.write("- 实时环境数据")
                st.write("- 预计收获时间")
    
    st.markdown("</div>", unsafe_allow_html=True)

# 4.5 会员民宿模块
elif page == "会员民宿模块":
    st.markdown("<h1 class='main-header'>会员民宿模块</h1>", unsafe_allow_html=True)
    st.markdown("<p>会员制乡村民宿，享受田园度假。</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 class='sub-header'>民宿预订</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 民宿选择
        st.subheader("选择民宿")
        location = st.selectbox("民宿地点", ["河北农庄", "山东农庄", "云南农庄"])
        
        # 根据地点显示不同民宿
        if location == "河北农庄":
            homestays = ["麦田小筑", "稻香阁", "果园别墅"]
            images = [
                "images/麦田小筑.png",
                "images/稻香阁.png",
                "images/果园别墅.png"
            ]
        elif location == "山东农庄":
            homestays = ["海风木屋", "渔村小院", "山顶观景房"]
            images = [
                "https://img.zcool.cn/community/01f7e75e2d6926a801216518a2d7e1.jpg@1280w_1l_2o_100sh.jpg",
                "https://img.zcool.cn/community/01c2ce5d0e9f8aa801219c7748b2b9.jpg@1280w_1l_2o_100sh.jpg",
                "https://img.zcool.cn/community/01d0f05af3c3c9a801219741f6c3a0.jpg@1280w_1l_2o_100sh.jpg"
            ]
        else:
            homestays = ["云端茶舍", "竹林别院", "花海木屋"]
            images = [
                "https://img.zcool.cn/community/031e2d75d8d65d0000012e7ed4b1c4.jpg",
                "https://img.zcool.cn/community/01f9c55d31a173a8012187f4c1f5ba.jpg@1280w_1l_2o_100sh.jpg",
                "https://img.zcool.cn/community/01a4a85af3c3c9a801219741cd7b8b.jpg@1280w_1l_2o_100sh.jpg"
            ]
        
        homestay = st.selectbox("民宿类型", homestays)
        homestay_idx = homestays.index(homestay)
        
        # 显示民宿图片
        st.image(images[homestay_idx], caption=homestay, use_container_width=True)
        
        # 预订信息
        st.subheader("预订信息")
        check_in = st.date_input("入住日期", datetime.now() + timedelta(days=1))
        days = st.number_input("入住天数", min_value=1, max_value=7, value=2)
        guests = st.number_input("入住人数", min_value=1, max_value=4, value=2)
        
        # 计算价格
        base_price = 300 if location == "河北农庄" else (400 if location == "山东农庄" else 500)
        total_price = base_price * days
        
        # 会员价格
        member_price = total_price * 0.7
        
        st.write(f"原价: ¥{total_price}/晚")
        st.write(f"会员价: ¥{member_price}/晚 (节省¥{total_price - member_price})")
        
        # 预订按钮
        if st.button("确认预订"):
            with st.spinner("正在处理预订请求..."):
                time.sleep(1)
                st.success(f"预订成功！您已预订{location}的{homestay}，入住日期{check_in.strftime('%Y-%m-%d')}，共{days}晚。")
                st.info(f"请在入住当天14:00后到达，凭预订信息办理入住。")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h2 class='sub-header'>会员权益</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 会员等级
        st.subheader("会员等级")
        membership = st.radio("选择会员类型", ["普通会员", "银卡会员", "金卡会员"])
        
        # 会员权益
        st.subheader("权益详情")
        if membership == "普通会员":
            price = "¥298/年"
            benefits = [
                "民宿7折优惠",
                "每年2次免费入住（每次限2天）",
                "农产品9折优惠",
                "专属会员活动"
            ]
        elif membership == "银卡会员":
            price = "¥598/年"
            benefits = [
                "民宿6折优惠",
                "每年4次免费入住（每次限2天）",
                "农产品8折优惠",
                "专属会员活动",
                "免费参加季度农事体验"
            ]
        else:
            price = "¥998/年"
            benefits = [
                "民宿5折优惠",
                "每年6次免费入住（每次限3天）",
                "农产品7折优惠",
                "专属会员活动",
                "免费参加所有农事体验",
                "专属定制农产品礼盒"
            ]
        
        st.write(f"会员费: {price}")
        st.write("会员权益:")
        for benefit in benefits:
            st.write(f"- {benefit}")
        
        # 加入会员
        if st.button("加入会员"):
            with st.spinner("正在处理会员申请..."):
                time.sleep(1)
                st.success(f"恭喜您成为{membership}！您将享受所有会员权益。")
        
        # 会员活动
        st.subheader("近期会员活动")
        st.write("1. 4月15日 - 春季采摘节")
        st.write("2. 5月1日 - 五一农耕体验")
        st.write("3. 6月1日 - 夏日露营之夜")
        
        st.markdown("</div>", unsafe_allow_html=True)

# 4.6 乡村亲子模块
elif page == "乡村亲子模块":
    st.markdown("<h1 class='main-header'>乡村亲子模块</h1>", unsafe_allow_html=True)
    st.markdown("<p>寓教于乐的乡村亲子活动，让孩子亲近自然。</p>", unsafe_allow_html=True)
    
    # 添加CSS样式使右侧年票固定
    st.markdown("""
    <style>
    .annual-pass-container {
        position: fixed;
        right: 2rem;
        top: 8rem;
        width: 25%;
        max-height: 85vh;
        overflow-y: auto;
        padding-right: 1rem;
        z-index: 1000;
    }
    .main-content {
        width: 70%;
        padding-right: 28%;
    }
    </style>
    """, unsafe_allow_html=True)

    # 主内容区域
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>亲子活动</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # 活动类型
    st.subheader("选择活动")
    activity_type = st.selectbox("活动类型", ["农耕体验", "自然探索", "手工制作", "科普课堂"])
    
    # 根据类型显示不同活动
    if activity_type == "农耕体验":
        activities = ["插秧体验", "蔬菜采摘", "喂养小动物"]
        # 显示农耕体验活动图片
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("images/插秧体验.png", caption="插秧体验", use_container_width=True)
        with col2:
            st.image("images/蔬菜采摘.png", caption="蔬菜采摘", use_container_width=True)
        with col3:
            st.image("images/喂养小动物.png", caption="喂养小动物", use_container_width=True)
    elif activity_type == "自然探索":
        activities = ["昆虫观察", "植物标本制作", "野外定向"]
    elif activity_type == "手工制作":
        activities = ["陶艺制作", "草编工艺", "农产品加工"]
    else:
        activities = ["农业科技课", "生态系统探索", "食品安全课堂"]
    
    activity = st.selectbox("具体活动", activities)
        
        # 活动详情
        # 活动详情
    st.subheader("活动详情")
    st.write(f"活动名称: {activity}")
    st.write("适合年龄: 5-12岁")
    st.write("活动时长: 2小时")
    st.write("活动地点: 河北农场教育中心")
        
        # 预订信息
    st.subheader("预订信息")
    date = st.date_input("活动日期", datetime.now() + timedelta(days=3))
    time_slot = st.selectbox("时间段", ["上午 9:00-11:00", "下午 14:00-16:00"])
    participants = st.number_input("参与人数", min_value=1, max_value=4, value=2)
        
        # 计算价格
    price_per_person = 80
    total_price = price_per_person * participants
        
        # 年票价格
    annual_pass_price = 300
        
    st.write(f"单次价格: ¥{total_price} (¥{price_per_person}/人)")
    st.write(f"年票价格: ¥{annual_pass_price}/年 (无限次参与，每次限4人)")
        
        # 预订按钮
    col1, col2 = st.columns(2)
    with col1:
            if st.button("单次预订"):
                with st.spinner("正在处理预订请求..."):
                    time.sleep(1)
                    st.success(f"预订成功！您已预订{date.strftime('%Y-%m-%d')} {time_slot}的{activity}活动，{participants}人参与。")
        
    with col2:
            if st.button("购买年票"):
                with st.spinner("正在处理年票购买请求..."):
                    time.sleep(1)
                    st.success(f"年票购买成功！您可以无限次参与所有亲子活动，有效期至{(datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')}。")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 固定在右侧的年票信息
    st.markdown("<div class='annual-pass-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>亲子年票</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # 年票权益
    st.subheader("年票权益")
    st.write("价格: ¥300/年")
    st.write("权益:")
    st.write("- 无限次参与所有亲子活动")
    st.write("- 每次最多4人同行")
    st.write("- 优先预订热门活动")
    st.write("- 专属亲子礼包")
    st.write("- 农场农产品9折优惠")
        
        # 近期活动日历
    st.subheader("近期活动日历")
    st.write("4月15日 - 春季插秧体验")
    st.write("4月22日 - 地球日特别活动")
    st.write("5月1日 - 劳动节农耕体验")
    st.write("5月15日 - 昆虫观察与标本制作")
    st.write("6月1日 - 儿童节特别活动")
        
        # 教育理念
    st.markdown("""
        <div class='info-msg'>
            <h4>教育理念</h4>
            <p>我们的亲子活动基于"自然教育"理念，让孩子在亲近自然的过程中，培养观察力、动手能力和环保意识，
            同时增进亲子关系，创造美好回忆。</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# 4.7 购物车
elif page == "购物车":
    st.markdown("<h1 class='main-header'>购物车</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("您的购物车还是空的，快去选购商品吧！")
    else:
        # 显示购物车商品
        st.subheader("购物车商品")
        
        # 创建表格显示购物车内容
        cart_df = pd.DataFrame(st.session_state.cart)
        st.write(cart_df)
        
        # 计算总价
        total = sum(item["total"] for item in st.session_state.cart)
        
        # 显示总价
        st.subheader(f"总计: ¥{total:.2f}")
        
        # 结算按钮
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("清空购物车"):
                st.session_state.cart = []
                st.success("购物车已清空！")
                st.rerun()
        
        with col2:
            if st.button("结算"):
                if st.session_state.user_logged_in:
                    with st.spinner("正在处理订单..."):
                        time.sleep(2)
                        st.success("订单已提交！感谢您的购买。")
                        st.session_state.cart = []
                        st.rerun()
                else:
                    st.error("请先登录后再结算！")

# 5. 主程序入口
if __name__ == "__main__":
    # 可以在这里添加初始化代码
    pass