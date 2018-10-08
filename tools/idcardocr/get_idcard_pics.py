import idcard_recognize as idr
import profile


if __name__ == '__main__':
    def run():
        res = idr.process('testimages/C_Q3hvni2asdSvlImTa1eqFM3hf7Hrj7db0Cp66s7fJBbmMvDkyJukS_lXDOvX_K.jpg')
        print(res)
    
    profile.run("run()")
