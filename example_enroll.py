#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import time
import hashlib
import pyfingerprint


## Enrolls new finger
##
def enroll_students():
    ## Tries to initialize the sensor
    try:
        f = pyfingerprint.PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            sha2Hash = hashlib.sha256(characterics).hexdigest()
            print('SHA-2 hash of template: ' + sha2Hash)
            # return sha2Hash;
            # print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        f.createTemplate()

        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        sha2Hash = hashlib.sha256(characterics).hexdigest()
        print('SHA-2 hash of template: ' + sha2Hash)
        return sha2Hash;

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

if __name__ == '__main__':
    main()