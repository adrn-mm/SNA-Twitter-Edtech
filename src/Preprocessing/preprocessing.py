# import library
import pandas as pd

# import dataset
df = pd.read_csv(
    r"c:\\Users\\LENOVO\\OneDrive\\Desktop\\Tugas Akhir\\Programming\\data\\raw/dataset.csv",
    low_memory=False,
)

# drop duplicate tweets
df = df.drop_duplicates("id")

# drop tweet that has no interaction
df = df[df.reply_to != "[]"]

# make reply_to (username and id) columns
df["reply_to_username"] = [
    eval(df.reply_to.tolist()[i])[0]["screen_name"] for i in range(0, df.shape[0])
]
df["reply_to_id"] = [
    eval(df.reply_to.tolist()[i])[0]["id"] for i in range(0, df.shape[0])
]
# take only user interaction
df = df[~df.username.str.contains("zeniuseducation|ruangguru")]
df = df[~df.reply_to_username.str.contains("zeniuseducation|ruangguru")]
# reset index in dataframe
df.reset_index(inplace=True, drop=True)

# group tweet based the tweet's context about ruangguru or zenius
df_zenius = df[
    (df.tweet.str.contains("zenius") == True)
    & ~df.tweet.str.contains("ruangguru|rg|ruang guru")
].copy()
df_ruangguru = df[
    df.tweet.str.contains("ruangguru|rg|ruang guru")
    == True & ~df.tweet.str.contains("zenius")
].copy()
# reset all df's index
df_zenius.reset_index(inplace=True, drop=True)
df_ruangguru.reset_index(inplace=True, drop=True)

# function to transform df to edge list form
def transform_edglst(df):
    # source and target column
    edglst = (
        df[["username", "reply_to_username"]]
        .copy()
        .rename(
            {"username": "Source", "reply_to_username": "Target"},
            # to lower case
            axis=1,
        )
        .applymap(lambda s: s.lower())
    )
    # weight column
    edglst = edglst.value_counts().to_frame("Weight").astype(float)
    return edglst.reset_index()


# apply the function
[edglst_ruangguru, edglst_zenius] = [
    transform_edglst(x) for x in [df_ruangguru, df_zenius]
]

# put the dfs to CSV form
edglst_ruangguru.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-preprocessing\ruangguru-edglst.csv",
    index=False,
    header=True,
)
edglst_zenius.to_csv(
    r"c:\Users\LENOVO\OneDrive\Desktop\Tugas Akhir\Programming\data\post-preprocessing\zenius-edglst.csv",
    index=False,
    header=True,
)
