while(1):
    text = input("Enter Text: ")
    Pt = ""
    Ct = ""
    for c in text:
        Ct += str(chr(ord(c)+1))
    print("CT: ", Ct)

    print("For Encrypt press 1")
    temp = input()
    if(temp == '1'):
        for c in Ct:
            Pt += str(chr(ord(c)-1))
        print("PT: ", Pt)
    elif(temp != "\n"):
        break



# text = input("Enter Text: ")
# Pt = ""
# Ct = ""
# for c in text:
#     # Pt.append(c)
#     Ct += str(chr(ord(c)+1))
#
# print("CT: ", Ct)
#
# for c in Ct:
#     Pt += str(chr(ord(c)-1))
#
# print("PT: ", Pt)