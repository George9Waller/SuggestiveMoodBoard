from peewee import *

import models


def addideas(board):
    # Tags
    FixtureType = models.Tag.create(Board=board, Name='Fixture Type', Colour='#c2571a')
    FixtureAngle = models.Tag.create(Board=board, Name='Fixture Angle', Colour='#107896')
    Scene1 = models.Tag.create(Board=board, Name='Scene 1', Colour='#9a2617')
    Scene2 = models.Tag.create(Board=board, Name='Scene 2', Colour='#168C40')
    Scene3 = models.Tag.create(Board=board, Name='Scene 3', Colour='#093145')
    Scene4 = models.Tag.create(Board=board, Name='Scene 4', Colour='#bca136')

    # Main ideas
    models.Idea.create(Name='Help', Content='This is a sample board based off a real project. It indicates the '
                                            'possibilities of what you can do on the platform. A key feature is the '
                                            'use of tags in the bar above, the bold box indicates the current filter '
                                            'and click another to only see ideas with that kind of data. Use the '
                                            'green box to create a new idea, but it must have a name and description, '
                                            'all other data is optional. Click on an idea to edit it or delete it and '
                                            'if you are done you can delete the whole board from the button at the '
                                            'top, be careful this cannot be undone. Finally you can always click the '
                                            'Suggestive Moodboard name to return to your boards, happy designing!',
                       Board=board, Colour='')

    Idea2 = models.Idea.create(Name='Tags',
                               Content='In this board I have used the 4 tags for the 4 main scenes in the piece, '
                                       'however they are meant to be versatile and used for anything you want, '
                                       'lighting related or not.',
                               Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea2, Tag=Scene1)
    models.Idea_Tag.create(Idea=Idea2, Tag=Scene2)
    models.Idea_Tag.create(Idea=Idea2, Tag=Scene3)
    models.Idea_Tag.create(Idea=Idea2, Tag=Scene4)

    Idea3 = models.Idea.create(Name='LED Strip',
                               Content='I will use LED strips along the floor to divide the stage into 4 '
                                       'columns, one for each character/group to represent the isolation in '
                                       'a Complicité style. They will be RGB controllable individually and '
                                       'I will use them in an abstract way to present conflict and control '
                                       'in the shoadows they create on actors and the strong harsh light '
                                       'for the audience.',
                               Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea3, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea3, Tag=FixtureAngle)

    Idea4 = models.Idea.create(Name='Torches', Content='To add a sense of control and searching I will use maglight torches '
                                               'held by each actor and used throughout the piece to convey their '
                                               'meaning. They also give off a warm white hue as they are incandescent '
                                               'which compliments skin very nicely when compared to cold white LED. '
                                               'They will be revealed in the opening of the piece in the void and and '
                                               'then left at the end when one character is left alone confused and '
                                               'paniced by their discovery.',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea4, Tag=FixtureType)

    models.Idea.create(Name='The Void', Content='The void is a very sterile and harsh environment where no shadows '
                                                'should be present, it is where the actors have gone after death and '
                                                'are searching for the meaning of their death/fate. This will be '
                                                'achieved through strong harsh white lighting from all angles as it '
                                                'is a surreal location. I will also use the LED tape to create a '
                                                'sense of isolation in the beginning, when the characters return at '
                                                'the end it will be even more harsh.',
                       Board=board, Colour='#ffffff')

    models.Idea.create(Name='Whites', Content='Complicité commonly use different shades of white in their pieces and '
                                              'I wanted to reflect this in my design. I have pathed a journey '
                                              'through my piece and decided what level of white should reflect the '
                                              'tension from 1-5 (warm white to cold) on a linear scale. In the most '
                                              'tense moments e.g. the void I use level 4/5 whites whereas in more '
                                              'familiar and pleasant moments e.g. graduation I use level 2 - its '
                                              'like the 7 levels of tension',
                       Board=board, Colour='#ffffff')

    # Graduation scene
    Idea5 = models.Idea.create(Name='Shuttering', Content='In the graduation the while the teachers are on the blocks I '
                                                  'wanted to emphasise the mental isolation from the main character '
                                                  'so I used square shuttering, inspired by A Disappearing Number to '
                                                  'enforce the separation visually. This is more noticeable in the '
                                                  'haze.',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea5, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea5, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea5, Tag=Scene1)

    Idea6 = models.Idea.create(Name='Jungle', Content='When Edie is being confronted by the hyenas (animalisation) there is a '
                                              'short sequence where there is a high level of abstraction, '
                                              'coupled with the torches, I created a dimly it jungle using back '
                                              'breakups and very dim single source green LED to show positional '
                                              'awareness through lighting.',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea6, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea6, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea6, Tag=Scene1)

    Idea7 = models.Idea.create(Name='Death', Content='When it is revealed Edie has died there is a strong change in tension, '
                                             'which I emphasised through a snap change to much colder lighting and '
                                             'strong isolation on his mother center stage.',
                       Board=board, Colour='#0000ff')
    models.Idea_Tag.create(Idea=Idea7, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea7, Tag=Scene1)

    Idea8 = models.Idea.create(Name='Blood', Content='When edie has died on the floor I used rear LED single source red '
                                             'lights which fade up to represent the blood pooling on the floor after '
                                             'being stabbed, this is then referenced in the dialogue.',
                       Board=board, Colour='#ff0000')
    models.Idea_Tag.create(Idea=Idea8, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea8, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea8, Tag=Scene1)

    # Boat
    Idea9 = models.Idea.create(Name='Boat scene colour', Content='In the second scene the setting is on a boat which catches '
                                                         'fire and sinks, to highlight this I used very strong hues '
                                                         'of blue throughout the scene and cold white for face light.',
                       Board=board, Colour='#0020ff')
    models.Idea_Tag.create(Idea=Idea9, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea9, Tag=Scene2)

    Idea10 = models.Idea.create(Name='Back light', Content='In the scene I reflected the tension and senario by using strong '
                                                  'backlight to shilouette the actors as the power is above them - '
                                                  'they have lost control in their death',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea10, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea10, Tag=Scene2)

    Idea11 = models.Idea.create(Name='Representing Boat', Content='The blocks which are used throughout the piece as '
                                                         'Complicité would are used in this scene as if the actor '
                                                         'were searching off the helm of the ship shining thee torch '
                                                         'through the haze to her husband she cant see drowning '
                                                         'downstage.',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea11, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea11, Tag=Scene2)

    Idea12 = models.Idea.create(Name='Cloth', Content='The blue cloth is used to represent the waves and moved as such, '
                                             'when the waves finally drown the character they shine their torch down '
                                             'the cloth as if they were a dot sinking to the bottom of the sea.',
                       Board=board, Colour='#0030ff')
    models.Idea_Tag.create(Idea=Idea12, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea12, Tag=Scene2)

    # Car
    Idea13 = models.Idea.create(Name='Abstract crash', Content='After the car has crashed the action of crashing is decomposed '
                                                      'and examined in the piece. I wanted to emphasis this by using '
                                                      'void-like lighting, especially from the back, to show again the '
                                                      'lack of power the characters face in their death which they '
                                                      'are searching for the meaning of.',
                       Board=board, Colour='#ffffff')
    models.Idea_Tag.create(Idea=Idea13, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea13, Tag=Scene3)

    Idea14 = models.Idea.create(Name='LED Lanes', Content='When transitioning into this scene the characters use the blocks as '
                                                 'steering wheels for cars and have a little competition in their '
                                                 'driving. I used the LED tape as the lane markings on the road which '
                                                 'gave more context and meaning to their movements, especially when '
                                                 'overtaking.',
                       Board=board, Colour='#ffffcf')
    models.Idea_Tag.create(Idea=Idea14, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea14, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea14, Tag=Scene3)

    Idea15 = models.Idea.create(Name='Pulses', Content='When breaking the crash into 3 stages I wanted to put embassies on '
                                              'the power of the crash even through they were analysing it slowly, '
                                              'when they announced each stage I had a really bright pulse of back '
                                              'light at the audience to show this power and significance in the event.',
                       Board=board, Colour='#ffffff')
    models.Idea_Tag.create(Idea=Idea15, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea15, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea15, Tag=Scene3)

    Idea16 = models.Idea.create(Name='The death', Content='When the crash has been decomposed the organs start to fail, '
                                                 'with each organ I snaped away 1/3 of the light until it was really '
                                                 'dim for the heart to stop (torches used to show heart stopping as a '
                                                 'fist) when it finally snapped to back for the next scene. It '
                                                 'craeted the effect of the body shutting down.',
                       Board=board, Colour='#111111')
    models.Idea_Tag.create(Idea=Idea16, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea16, Tag=Scene3)

    # Train
    Idea17 = models.Idea.create(Name='Transition into Train', Content='For the transition into the train we created a physical '
                                                             'sequence of a train with workers. I brought across this '
                                                             'atmosphere in lighting through back amber lighting from '
                                                             'lights on the floor at the back which lit the haze and '
                                                             'the beams were split by the blocks infront.',
                       Board=board, Colour='#ff2200')
    models.Idea_Tag.create(Idea=Idea17, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea17, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea17, Tag=Scene4)

    Idea18 = models.Idea.create(Name='Mind the doors', Content='For when the doors of the train close there is a moment of '
                                                      'stress which I wanted to portray by a snap transition from '
                                                      'lighting only up stage to mainly lighting mid stage. This was '
                                                      'difficult toisolate in such a small venue, but I used the side '
                                                      'LEDs to emphasise the change',
                       Board=board, Colour='')
    models.Idea_Tag.create(Idea=Idea18, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea18, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea18, Tag=Scene4)

    Idea19 = models.Idea.create(Name='Running out of Time', Content='When the stress of daily life starts to amount the main '
                                                           'character starts to forget what they want to say and '
                                                           'looses communication with the rest of the people. As the '
                                                           'stress intensified I faded up rear blue lights to again '
                                                           'highlight the higher power and add to the '
                                                           'tension/abstraction before snapping to a white void state '
                                                           '(peak tension) before the crash',
                       Board=board, Colour='#1000ff')
    models.Idea_Tag.create(Idea=Idea19, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea19, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea19, Tag=Scene4)

    Idea20 = models.Idea.create(Name='The crash', Content='When the bomb goes off there is a high pitched sound and a sudden '
                                                 'burst of light form the downstage left side parcan with lavender '
                                                 'gel, this then trasnitions into all the side lights and back light '
                                                 'to show the leaast power in the whole piece through the shadows '
                                                 'across the acors faces and sihlouettes from behind. It is meant to '
                                                 'be the most painful moment of the whole piece before snapping back '
                                                 'to the final void.',
                       Board=board, Colour='#ff2220')
    models.Idea_Tag.create(Idea=Idea20, Tag=FixtureType)
    models.Idea_Tag.create(Idea=Idea20, Tag=FixtureAngle)
    models.Idea_Tag.create(Idea=Idea20, Tag=Scene4)