# Bank Management System

<https://bank.yusanshi.com/>

A simple bank management system in Vue.js and Flask.

## Get started

```bash
git clone https://github.com/yusanshi/bank-management-system && cd bank-management-system

# Backend
cd backend
pip install -r requirements.txt
python wsgi.py

# Frontend
# Use ctrl+shift+T to open a new tab
cd ../frontend
yarn install
yarn serve
```

## Credits

- Icons: [Kiranshastry](https://www.flaticon.com/authors/kiranshastry)
- Dashboard: [vue-material-admin](https://github.com/tookit/)






> **实验要求**
>
> 某银行准备开发一个银行业务管理系统。该银行的数据需求与 Lab 02 相同。下面要求为该银行开发业务管理系统。
>
> **数据需求**
>
> 银行有多个支行。各个支行位于某个城市,每个支行有唯一的名字。银行要监控每个支行的资产。 银行的客户通过其身份证号来标识。银行存储每个客户的姓名、联系电话以及家庭住址。为了安全起见,银行还要求客户提供一位联系人的信息,包括联系人姓名、手机号、Email 以及与客户的关系。客户可以有帐户,并且可以贷款。客户可能和某个银行员工发生联系,该员工是此客户的贷款负责人或银行帐户负责人。银行员工也通过身份证号来标识。员工分为部门经理和普通员工,每个部门经理都负责领导其所在部门的员工,并且每个员工只允许在一个部门内工作。每个支行的管理机构存储每个员工的姓名、电话号码、家庭地址、所在的部门号、部门名称、部门类型及部门经理的身份证号。银行还需知道每个员工开始工作的日期,由此日期可以推知员工的雇佣期。银行提供两类帐户——储蓄帐户和支票帐户。帐户可以由多个客户所共有,一个客户也可开设多个账户,但在一个支行内最多只能开设一个储蓄账户和一个支票账户。每个帐户被赋以唯一的帐户号。银行记录每个帐户的余额、开户日期、开户的支行名以及每个帐户所有者访问该帐户的最近日期。另外,每个储蓄帐户有利率和货币类型,且每个支票帐户有透支额。每笔贷款由某个分支机构发放,能被一个或多个客户所共有。每笔贷款用唯一的贷款号标识。银行需要知道每笔贷款所贷金额以及逐次支付的情况(银行将贷款分几次付给客户)。虽然贷款号不能唯一标识银行所有为贷款所付的款项,但可以唯一标识为某贷款所付的款项。对每次的付款需要记录日期和金额。
>
> **功能需求**
>
> - 客户管理:提供客户所有信息的增、删、改、查功能;如果客户存在着关联账户或者贷款记录,则不允许删除;
>
> - 账户管理:提供账户开户、销户、修改、查询功能,包括储蓄账户和支票账户;账户号不允许修改;
>
> - 贷款管理:提供贷款信息的增、删、查功能,提供贷款发放功能;贷款信息一旦添加成功后不允许修改;要求能查询每笔贷款的当前状态(未开始发放、发放中、已全部发放);处于发放中状态的贷款记录不允许删除;
>
> - 业务统计:按业务分类(储蓄、贷款)和时间(月、季、年)统计各个支行的业务总金额和用户数,要求对统计结果同时提供表格和曲线图两种可视化展示方式。
>
> **说明**
>
> 1. 支行、部门和员工的信息需要预先插入到数据库中,本项目假设这三类数据已经在数据库中了,并且本实验不要求实现这三类数据的维护。
> 2. 后台 DBMS 使用 MySQL;
> 3. 前端开发工具不限,可以是 C/S 架构也可以是 B/S 架构;
> 4. 查询功能允许自行设计,但要求尽可能灵活设计,考虑用户多样化的查询需求;
> 5. 各类数据的类型可自行根据实际情况设计;
> 6. 测试数据自行设计;
> 7. 系统实现时要保证数据之间的一致性;
> 8. 程序须有一定的出错处理,要求自己先做好测试,能够处理可以预见的一些错误,例如输入的客户姓名带单引号(类似 O’Neil)、输入数据不合法等等;
> 9. 其余功能可以自行添加,例如登录管理、权限管理等等,但不做强制要求。如果做了添加,请在实验报告中加以描述;
> 10. 本实验要求单独完成。