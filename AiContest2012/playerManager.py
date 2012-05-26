# coding: cp932
from ymzkgame.runnable import Runnable
from ymzkgame.manager import Manager
from gameConfig import UNIT_MAX_SPEED, UNIT_MAX_ROLL_ANGLE

class PlayerManager(Runnable):
  '''AiManager�̂ӂ�����ăL�[���͂��瓮���𐶐�����N���X'''
  def __init__(self):
    Runnable.__init__(self)
    self.speed = UNIT_MAX_SPEED
    self.rollAngle = UNIT_MAX_ROLL_ANGLE
    self.moveKeys = (Manager.K_UP, Manager.K_w)
    self.leftRollKeys = (Manager.K_LEFT, Manager.K_a)
    self.rightRollKeys = (Manager.K_RIGHT, Manager.K_d)
    self.fireKeys = (Manager.K_SPACE, Manager.K_z, Manager.K_DOWN, Manager.K_s, Manager.K_z, Manager.K_x, Manager.K_LSHIFT, Manager.K_RSHIFT)
  def step(self):
    '''AiManager���̎��Ԃ��P�t���[���i�߂郁�\�b�h
AI�ւ̏������݁A�ǂݍ��݂̓^�C�~���O���V�r�A�Ȃ̂ŁAwriteMessage�AreadMessage�͏�ʂ̃N���X���璼�ڌĂ΂��@�����̃��\�b�h������Ă�ł͂����Ȃ�
�܂�����������Ȃ�
�I�[�o�[���C�h���Ȃ��ƃG���[�ɂȂ�(Runnable�̎d�l)'''
  def end(self):
    '''AiManager�̏I�������������Ƃ���
�I�[�o�[���C�h����K�v�͂Ȃ�
Runnable��end���Ă΂�Ȃ��Ɖ������N���邩������Ȃ�'''
    Runnable.end(self)
  def sendEndMessage(self, unit, manager):
    '''AI�ɃQ�[���I����ʒm�����郁�\�b�h
�Q�[���I�����ɌĂ΂��
Unit�ɂ���ČĂяo����A�����Ŏ󂯎����GameManager��Unit�̃��\�b�h���Ă�ŏ��𓾂�B��d�l�B'''
    pass
  def sendStartingMessage(self, unit, manager):
    '''AI�ɏ������p�̃f�[�^�𑗂点�郁�\�b�h
�Q�[���J�n���ɌĂ΂��
Unit�ɂ���ČĂяo����A�����Ŏ󂯎����GameManager��Unit�̃��\�b�h���Ă�ŏ��𓾂�B��d�l�B'''
    pass
  def writeMessage(self, unit, manager):
    '''AI�Ɍ��݂̃Q�[�����̏󋵂𑗂点�郁�\�b�h
���t���[���Ă΂��
Unit�ɂ���ČĂяo����A�����Ŏ󂯎����GameManager��Unit�̃��\�b�h���Ă�ŏ��𓾂�B��d�l�B'''
    pass
  def readMessage(self):
    '''AI����̃��b�Z�[�W��ǂ�œ�����Ԃ��X�V���郁�\�b�h
���̃��\�b�h���Ă΂��ƁAgetMove�AgetRotate�AgetFiring�̌��ʂ��ω�����
�ʓ|�Ȃ̂œ��͂̓ǂݍ��݂͂����ł͂��܂���'''
    pass
  def getMove(self):
    '''���̃t���[���Ƀ��j�b�g�����ۂɈړ����鑬����\������������Ԃ����\�b�h
����̃`�F�b�N�͂����ł��Ȃ��Ƃ����Ȃ�
������readMessage�ƌ��݂ɁA���t���[����񂾂��Ă΂��'''
    if self._checkKeys(self.moveKeys):
      return self.speed
    return 0
  def getRotate(self):
    '''���̃t���[���Ƀ��j�b�g�����ۂɉ�]����ʂ�\������������Ԃ����\�b�h
�s���ȉ�]�͂����Ń`�F�b�N���Ȃ��Ƃ����Ȃ�
������readMessage�ƌ��݂ɁA���t���[����񂾂��Ă΂��'''
    result = 0
    if self._checkKeys(self.rightRollKeys):
      result += self.rollAngle
    if self._checkKeys(self.leftRollKeys):
      result -= self.rollAngle
    return result
  def getFiring(self):
    '''���̃t���[����AI���U�����������ǂ�����\���^�U�l��Ԃ����\�b�h
�U���Ԋu�̐���͏�ʂ̃N���X������Ă����'''
    return self._checkKeys(self.fireKeys)
  def _checkKeys(self, keys):
    return any(Manager.getKeyStatus(key) for key in keys)
