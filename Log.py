
from RebotConfig import RebotConfig
# 

class Log():

    @staticmethod
    def d(content):
        f = open('%s%s' % (RebotConfig.path, RebotConfig.log), 'a+');
        f.write('%s\n' % content)
        f.close();
        print content;
