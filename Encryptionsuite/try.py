import os

'''
def _clean_dir_(gdir, mode):
    try:
        # Delete all original files
        for root, dirs, files in os.walk(gdir):
            for file in files:
                _path_ = os.path.join(root, file)

                # Clean enc files
                if mode is True:

                    print(_path_[:-1].endswith('enc') and os.path.exists(_path_[:-5]))
                    if _path_[:-1].endswith('enc') and os.path.exists(_path_[:-5]):
                        print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
                        #os.remove(_path_)

                # Clean original files
                if mode is False:

                    if not _path_[:-1].endswith('enc') and (os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}')):
                        print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
                    j = _path_[-1:]
                    x = _path_[-1:]
                    print(j, x)
                    print(_path_[:-1].endswith('enc') and os.path.exists(_path_ + f'.enc{x}') and os.path.exists(_path_ + f'.enc{j}'))
                    if _path_[:-1].endswith('enc') and os.path.exists(_path_ + f'.enc{x}') and os.path.exists(_path_ + f'.enc{j}') and j > x:
                        print(f"Rm{_path_ + f'.enc{x}'} in favour of {_path_ + f'.enc{j}'}")
                        # os.remove(_path_)

    except Exception as e:
        print(f"\033[31m{e}\033[0m")
    finally:
        print("\033[92mSucceed✅\033[0m")

'''
#print("Status:", end='')
import time
pr = "hello: "
for i in range(10):
    print(f'{pr}{i}', end='\r')
    time.sleep(1)
