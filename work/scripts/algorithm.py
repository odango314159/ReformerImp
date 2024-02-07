## 変更できる場所としてはnum_lengthをコンストラクタで定義するかどうか
## 定義しておけば変換が可逆になる(元の行列に戻したい時にできるようになる)
## 定義しなければ引数で与えるものが少なくなるので呼び出しが楽になる
import torch
import numpy as np
class Calculate_LSH:
    def __init__(
        self,
        d_model:int,
        num_length:int,
        num_buckets:int,
    )->None:
        ## define random matrix for rotation
        self.R = np.random.randn(d_model,int(num_buckets/2))
        ## define vectors to store labels
        ## ここは別にハッシュ計算部分で個別に定義してもいいけど変換を可逆にしたい時に便利かなって思ったのでこうしてます
        self.labels = torch.randint(high=num_buckets,size=(num_length,))
    def raw_to_sorted_data(
        self,
        input:torch.tensor,
    )-> torch.tensor:
        ##requires->行列
        ##effects->ハッシュを元に各ベクトルのラベルを求め、ラベルごとに行列をソート
        self.labels = self.__cal_hash(input)
        sorted_indices = self.labels.argsort()
        return input[sorted_indices]
    def __cal_hash(
        self,
        input:torch.tensor,
    )-> torch.tensor:
        ## requires->行列
        ## effects->ハッシュを計算、単語ごとにハッシュを割り当ててラベルベクトルとして返す。
        x_R = input@self.R
        x_R = torch.cat([x_R, -x_R], dim=1)
        ## argmaxに書き換えてもいいけどmax使った方がhashの値まで見えていいかなと思ってこっちにしてる
        hash = torch.max(x_R,dim=1).indices
        return hash