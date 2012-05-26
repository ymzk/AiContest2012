# coding: cp932
from ymzkgame.runnable import Runnable
from ymzkgame.manager import Manager
from gameConfig import UNIT_MAX_SPEED, UNIT_MAX_ROLL_ANGLE

class PlayerManager(Runnable):
  '''AiManagerのふりをしてキー入力から動きを生成するクラス'''
  def __init__(self):
    Runnable.__init__(self)
    self.speed = UNIT_MAX_SPEED
    self.rollAngle = UNIT_MAX_ROLL_ANGLE
    self.moveKeys = (Manager.K_UP, Manager.K_w)
    self.leftRollKeys = (Manager.K_LEFT, Manager.K_a)
    self.rightRollKeys = (Manager.K_RIGHT, Manager.K_d)
    self.fireKeys = (Manager.K_SPACE, Manager.K_z, Manager.K_DOWN, Manager.K_s, Manager.K_z, Manager.K_x, Manager.K_LSHIFT, Manager.K_RSHIFT)
  def step(self):
    '''AiManager内の時間を１フレーム進めるメソッド
AIへの書き込み、読み込みはタイミングがシビアなので、writeMessage、readMessageは上位のクラスから直接呼ばれる　※このメソッド内から呼んではいけない
つまり実質何もしない
オーバーライドしないとエラーになる(Runnableの仕様)'''
  def end(self):
    '''AiManagerの終了処理を書くところ
オーバーライドする必要はない
Runnableのendが呼ばれないと何かが起きるかもしれない'''
    Runnable.end(self)
  def sendEndMessage(self, unit, manager):
    '''AIにゲーム終了を通知させるメソッド
ゲーム終了時に呼ばれる
Unitによって呼び出され、引数で受け取ったGameManagerとUnitのメソッドを呼んで情報を得る。謎仕様。'''
    pass
  def sendStartingMessage(self, unit, manager):
    '''AIに初期化用のデータを送らせるメソッド
ゲーム開始時に呼ばれる
Unitによって呼び出され、引数で受け取ったGameManagerとUnitのメソッドを呼んで情報を得る。謎仕様。'''
    pass
  def writeMessage(self, unit, manager):
    '''AIに現在のゲーム内の状況を送らせるメソッド
毎フレーム呼ばれる
Unitによって呼び出され、引数で受け取ったGameManagerとUnitのメソッドを呼んで情報を得る。謎仕様。'''
    pass
  def readMessage(self):
    '''AIからのメッセージを読んで内部状態を更新するメソッド
このメソッドが呼ばれると、getMove、getRotate、getFiringの結果が変化する
面倒なので入力の読み込みはここではしません'''
    pass
  def getMove(self):
    '''このフレームにユニットが実際に移動する速さを表す浮動小数を返すメソッド
上限のチェックはここでしないといけない
きっとreadMessageと交互に、毎フレーム一回だけ呼ばれる'''
    if self._checkKeys(self.moveKeys):
      return self.speed
    return 0
  def getRotate(self):
    '''このフレームにユニットが実際に回転する量を表す浮動小数を返すメソッド
不正な回転はここでチェックしないといけない
きっとreadMessageと交互に、毎フレーム一回だけ呼ばれる'''
    result = 0
    if self._checkKeys(self.rightRollKeys):
      result += self.rollAngle
    if self._checkKeys(self.leftRollKeys):
      result -= self.rollAngle
    return result
  def getFiring(self):
    '''このフレームにAIが攻撃したいかどうかを表す真偽値を返すメソッド
攻撃間隔の制御は上位のクラスがやってくれる'''
    return self._checkKeys(self.fireKeys)
  def _checkKeys(self, keys):
    return any(Manager.getKeyStatus(key) for key in keys)
