import v2

def main():

# source = '0' pour la webcam du pc , @ip pour une camera ip 
    v2.finger_stream(source='https://192.168.48.183:8080/video')

if __name__ == '__main__':
    main() 
