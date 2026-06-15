import pandas as pd

def prepare_retention(activity):
    # step1: calculate cohort
    first_day = (
        activity.groupby("user_id")["activity_date"]
        .min()
        .reset_index()
        .rename(
            columns=
            {
                "activity_date":"first_day"
            }
        )
    )
    print(first_day)
    # merge two 
    activity = activity.merge(
        first_day,
        on="user_id"
    )
    print(activity)
    # step2: calculate retained_days
    activity["retention_day"]=(
        activity["activity_date"] - activity["first_day"]
    ).dt.days
    print(activity)
    return activity

def calculate_retention(activity,day):
    # retention_rate=某天仍留存的用户数 / 新增用户数
    # step1 :计算新增用户数
    new_users = activity[
        activity["retention_day"]==0
        ].groupby("first_day")["user_id"].nunique()
    print(new_users)
    # step2 :求解用户day留存
    retained_days = activity[
        activity["retention_day"] == day
    ].groupby("first_day")["user_id"].nunique()
    print(retained_days)
    retention_rate = (
        retained_days
        .div(new_users)
        .fillna(0)
    )* 100
    print(retention_rate)
    return retention_rate

def build_retention_matrix(activity):
    # step1: 统计所有留存天数
    retention = (
        activity.groupby(
            ["first_day","retention_day"]
        )["user_id"].nunique()
    )
    print(retention)
    # step2: 将数据表展开成矩阵
    retention_count = (
        retention
        .unstack(fill_value=0)
    )
    print(retention_count)
    # step3： 计算留存率= 每行的值 / 每行第一个值
    retention_rate = (
        retention_count
        .div(retention_count[0],axis=0)
        .fillna(0)
        .mul(100)
        .round(2)
    )
    print(retention_rate)
    return retention_rate

if __name__ == "__main__":
     # read data
    activity = pd.DataFrame({
        "user_id":[1,1,2,2,3,3,3,4,5],
        "activity_date":[
            "2025-01-01",
            "2025-01-02",
            "2025-01-01",
            "2025-01-03",
            "2025-01-02",
            "2025-01-03",
            "2025-01-09",
            "2025-01-05",
            "2025-01-05"
        ]
    })
    # turn str to date
    activity["activity_date"]=pd.to_datetime(activity["activity_date"])
    activity = prepare_retention(activity)
    day1_rate = calculate_retention(activity,1)
    retention_rate = build_retention_matrix(activity)
    # modify column name
    retention_rate.columns = [
        f"Day:{day}" 
        for day in retention_rate.columns
    ]
        # save to csv
    retention_rate.to_csv("Retention-Analysis/retention_rate.csv")
    print("保存成功！")