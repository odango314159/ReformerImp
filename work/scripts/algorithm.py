# 変更できる場所としてはnum_lengthをコンストラクタで定義するかどうか
# 定義しておけば変換が可逆になる(元の行列に戻したい時にできるようになる)
# 定義しなければ引数で与えるものが少なくなるので呼び出しが楽になる
import torch
from torch import nn


class Calculate_LSH(nn.Module):
    def __init__(
        self,
        d_model: int,
        num_length: int,
        num_buckets: int,
    ) -> None:
        super().__init__()
        # define random matrix for rotation
        self.R = torch.randn(size=(d_model, int(num_buckets / 2)))
        # define vectors to store labels
        # ここは別にハッシュ計算部分で個別に定義してもいいけど変換を可逆にしたい時に便利かなって思ったのでこうしてます
        self.labels = torch.randint(high=num_buckets, size=(num_length,))

    def forward(
        self,
        input: torch.tensor,
    ) -> torch.tensor:
        # requires->行列
        # effects->ハッシュを元に各ベクトルのラベルを求め、ラベルごとに行列をソート
        self.labels = self.__cal_hash(input)
        sorted_indices = self.labels.argsort()
        input = torch.index_select(input, 0, sorted_indices)
        return input

    def __cal_hash(
        self,
        input: torch.tensor,
    ) -> torch.tensor:
        # requires->行列
        # effects->ハッシュを計算、単語ごとにハッシュを割り当ててラベルベクトルとして返す。
        x_R = input @ self.R
        x_R = torch.cat([x_R, -x_R], dim=1)
        # argmaxに書き換えてもいいけどmax使った方がhashの値まで見えていいかなと思ってこっちにしてる
        hash = torch.max(x_R, dim=1).indices
        return hash
