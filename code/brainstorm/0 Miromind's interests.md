Let's add some info about the Miro so that you can know what's the interests and inclination of them.


"一、官方核心资源（第一手信息）
1. 官方网站与博客
官网：https://www.miromind.ai/
包含 MiroThinker-H1 的完整技术架构图（DAG 推理链、验证器设计）
最新基准测试数据和产品路线图
官方技术博客：https://miromind.ai/blog/
已发布：《MiroFlow v0.2: 开源深度研究 Agent 框架》（2025.8）
后续会更新 v1.7 的技术细节和验证机制的深入解析
2. 开源生态（全部免费可用）
表格
项目	链接	核心内容
MiroThinker 模型仓库	https://github.com/MiroMindAI/MiroThinker	v1.0/v1.5/v1.7 全版本代码、部署指南、评测脚本
MiroFlow Agent 框架	https://github.com/MiroMindAI/MiroFlow	可将任意 LLM 升级到 Deep Research 级能力，单 RTX 4090 即可运行
MiroVerse 数据集	https://huggingface.co/datasets/miromind-ai/MiroVerse-v0.1	147K + 条完整 Agent 交互轨迹，包含 SFT 和 DPO 训练数据
HuggingFace 模型页	https://huggingface.co/collections/miromind-ai/mirothinker-17	8B/30B/72B/235B 全尺寸模型权重，支持直接下载部署
3. 其他官方论文
MiroMind-M1 数学推理模型：arXiv:2507.14683v1
开源了完整的数学验证器和训练超参数，分享了大量训练 "踩坑" 经验
MiroFlow 框架论文：随 GitHub 仓库发布，详细介绍了高并发 Agent 编排和容错设计
二、第三方深度技术解读
1. 技术路线与哲学分析
《MiroMind 破局：在大语言模型的夹缝中，陈天桥在造什么？》（工控网，2026.2）
陈天桥首次系统阐述 "通用推理引擎" 定位，反对主流的 "行为主义" 和 "功能主义" 路线
提出 "逻辑长征" 概念：将算力用于 "时间序列上的反复求证" 而非一次性生成长文
《30B 参数碾压 1T 模型？MiroThinker 1.5 用 "科学家模式" 颠覆 AI 开发》（CSDN，2026.6）
深度对比 "做题家模式"（传统大模型）与 "科学家模式"（MiroMind）的本质区别
详细分析了交互式扩展如何用 1/30 的参数实现万亿级模型的性能
2. v1.7 验证机制专项解读
《当 AI 学会了验证自己的推理》（人人都是产品经理，2026.3）
拆解了局部验证 + 全局验证的具体实现方式
补充了超级碗、格莱美等更多预测案例的推理过程
《MiroThinker-1.7 & H1：验证为中心的重型推理时代》（PR Newswire 官方新闻稿，2026.3）
官方发布的最权威技术说明，包含完整的基准测试对比表
3. 工程实现细节
《MiroThinker：开源 AI 研究助手实现交互式推理突破》（CSDN，2026.5）
详细介绍了 256K 上下文管理和 600 次工具调用的工程实现
对比了 MiroThinker 与其他开源研究 Agent 的架构差异
《MiroMind 发布 M1 系列：会思考的 AI 数学天才是如何炼成的》（CSDN，2026.5）
分享了训练过程中的关键超参数（学习率 5×10^-5、3 轮训练、批次大小 128）
开源了改进的数学验证器代码
三、行业报道与最新动态
1. 重要事件报道
2026 年 5 月暂停中国区服务：
新浪财经：《突发！陈天桥旗下 MiroMind AI 暂停中国服务》
腾讯新闻：《陈天桥旗下 MiroMind 5 月 12 日起暂停大陆港澳服务》
核心原因：Manus 事件后的监管压力，已实施中美业务全面防火墙
2026 年 4 月代季峰离职事件：
钛媒体独家：《突发！代季峰与陈天桥矛盾激化，离职 MiroMind 真相曝光》
涉及股权纠纷和技术团队拆分，对 MiroMind 后续研发有一定影响
2. 社区与交流渠道
Discord 官方频道：https://discord.gg/F7EQFnYscV
有 #everything-prediction 专区，分享各类预测案例和推理过程
技术文档站：https://miromindai.github.io/MiroFlow/
包含 MiroFlow 完整的 API 文档、部署教程和最佳实践"

Please summary the information of the hackthon again about the whole context of the comeptition.

I have some ideas:

1. We should consider the interests of the MiroMind, because they are responsor chasing for their next goal. 
2. I notice that the official use of Miro is to "prediction" along with time series, and interactive review for high quality. 
3. It's good for long time deep research. So our hackthon demo should follow the way the model was designed to, and join the data flywheel in their mindset. 
4. Even they care more about business data, I still think human situation (my survivor self help idea) is worth considering. Because the usage data is what they lack after consuming the high quality data.




