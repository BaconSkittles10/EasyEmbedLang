from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import random

from eel.values import Number, Null, String, BaseType, List


class RandomModule(EelModule):
    @staticmethod
    @eel_function
    def randrange(start, stop=Null(), step=Number(1)):
        return RTResult().success(Number(random.randrange(start.value, stop.value, step.value)))

    @staticmethod
    @eel_function
    def randint(start, stop):
        return RTResult().success(Number(random.randint(start.value, stop.value)))

    @staticmethod
    @eel_function
    def choice(list_):
        return RTResult().success(random.choice(list_.elements))

    @staticmethod
    @eel_function
    def shuffle(list_):
        random.shuffle(list_.elements)
        return RTResult().success(Null())

    @staticmethod
    def sample(self):  # TODO
        pass

    @staticmethod
    @eel_function
    def uniform(start, stop):
        return RTResult().success(Number(random.uniform(start.value, stop.value)))

    @staticmethod
    @eel_function
    def triangular(low=Number(0.0), high=Number(1.0), mode=None):
        return RTResult().success(Number(random.triangular(low.value, high.value, mode)))

    @staticmethod
    @eel_function
    def normalvariate(mu=Number(0.0), sigma=Number(1.0)):
        return RTResult().success(Number(random.normalvariate(mu.value, sigma.value)))

    @staticmethod
    @eel_function
    def gauss(mu=Number(0.0), sigma=Number(1.0)):
        return RTResult().success(Number(random.gauss(mu.value, sigma.value)))

    @staticmethod
    @eel_function
    def lognormvariate(mu, sigma):
        return RTResult().success(Number(random.lognormvariate(mu.value, sigma.value)))

    @staticmethod
    @eel_function
    def expovariate(lambd=Number(1.0)):
        return RTResult().success(Number(random.expovariate(lambd.value)))

    @staticmethod
    @eel_function
    def vonmisesvariate(mu, kappa):
        return RTResult().success(Number(random.vonmisesvariate(mu.value, kappa.value)))

    @staticmethod
    @eel_function
    def gammavariate(alpha, beta):
        return RTResult().success(Number(random.vonmisesvariate(alpha.value, beta.value)))

    @staticmethod
    @eel_function
    def betavariate(alpha, beta):
        return RTResult().success(Number(random.betavariate(alpha.value, beta.value)))

    @staticmethod
    @eel_function
    def paretovariate(alpha):
        return RTResult().success(Number(random.paretovariate(alpha.value)))

    @staticmethod
    @eel_function
    def weibullvariate(alpha, beta):
        return RTResult().success(Number(random.weibullvariate(alpha.value, beta.value)))

    @staticmethod
    @eel_function
    def binomialvariate(n=Number(1), p=Number(0.5)):
        return RTResult().success(Number(random.binomialvariate(n.value, p.value)))


RandomModule.initialize()
