from peewee import *

import models


def addideas(board):
    # Tags
    FixtureType = models.Tag.create_tag(board=board, name='Fixture Type', colour='#c2571a')
    FixtureAngle = models.Tag.create_tag(board=board, name='Fixture Angle', colour='#107896')
    Scene1 = models.Tag.create_tag(board=board, name='Scene 1', colour='#9a2617')
    Scene2 = models.Tag.create_tag(board=board, name='Scene 2', colour='#168C40')
    Scene3 = models.Tag.create_tag(board=board, name='Scene 3', colour='#093145')
    Scene4 = models.Tag.create_tag(board=board, name='Scene 4', colour='#bca136')

    # Main ideas
    models.Idea.create_idea(name='Help', content='This is a sample board based off a real project. It indicates the '
                                            'possibilities of what you can do on the platform. A key feature is the '
                                            'use of tags in the bar above, the bold box indicates the current filter '
                                            'and click another to only see ideas with that kind of data. Use the '
                                            'green box to create a new idea, but it must have a name, '
                                            'all other data is optional. Click on an idea to edit it or delete it and '
                                            'if you are done you can delete the whole board from the button at the '
                                            'top, be careful this cannot be undone. Click the flask icon to view the '
                                            'colour suggestions for your board - they may be interesting and spark '
                                            'a new idea. Finally you can always click the '
                                            'Suggestive Moodboard name to return to your boards, happy designing!',
                       board=board, colour='')

    idea2 = models.Idea.create_idea(name='Tags',
                               content='In this board I have used the 4 tags for the 4 main scenes in the piece, '
                                       'however they are meant to be versatile and used for anything you want, '
                                       'lighting related or not.',
                               board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea2, tag=Scene1)
    models.Idea_Tag.create_idea_tag_link(idea=idea2, tag=Scene2)
    models.Idea_Tag.create_idea_tag_link(idea=idea2, tag=Scene3)
    models.Idea_Tag.create_idea_tag_link(idea=idea2, tag=Scene4)

    idea3 = models.Idea.create_idea(name='LED Strip',
                               content='I will use LED strips along the floor to divide the stage into 4 '
                                       'columns, one for each character/group to represent the isolation in '
                                       'a Complicité style. They will be RGB controllable individually and '
                                       'I will use them in an abstract way to present conflict and control '
                                       'in the shoadows they create on actors and the strong harsh light '
                                       'for the audience.',
                               board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea3, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea3, tag=FixtureAngle)

    idea4 = models.Idea.create_idea(name='Torches', content='To add a sense of control and searching I will use maglight torches '
                                               'held by each actor and used throughout the piece to convey their '
                                               'meaning. They also give off a warm white hue as they are incandescent '
                                               'which compliments skin very nicely when compared to cold white LED. '
                                               'They will be revealed in the opening of the piece in the void and and '
                                               'then left at the end when one character is left alone confused and '
                                               'paniced by their discovery.',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea4, tag=FixtureType)

    models.Idea.create_idea(name='The Void', content='The void is a very sterile and harsh environment where no shadows '
                                                'should be present, it is where the actors have gone after death and '
                                                'are searching for the meaning of their death/fate. This will be '
                                                'achieved through strong harsh white lighting from all angles as it '
                                                'is a surreal location. I will also use the LED tape to create a '
                                                'sense of isolation in the beginning, when the characters return at '
                                                'the end it will be even more harsh.',
                       board=board, colour='#ffffff')

    models.Idea.create_idea(name='Whites', content='Complicité commonly use different shades of white in their pieces and '
                                              'I wanted to reflect this in my design. I have pathed a journey '
                                              'through my piece and decided what level of white should reflect the '
                                              'tension from 1-5 (warm white to cold) on a linear scale. In the most '
                                              'tense moments e.g. the void I use level 4/5 whites whereas in more '
                                              'familiar and pleasant moments e.g. graduation I use level 2 - its '
                                              'like the 7 levels of tension',
                       board=board, colour='#ffffff')

    # Graduation scene
    idea5 = models.Idea.create_idea(name='Shuttering', content='In the graduation the while the teachers are on the blocks I '
                                                  'wanted to emphasise the mental isolation from the main character '
                                                  'so I used square shuttering, inspired by A Disappearing Number to '
                                                  'enforce the separation visually. This is more noticeable in the '
                                                  'haze.',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea5, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea5, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea5, tag=Scene1)

    idea6 = models.Idea.create_idea(name='Jungle', content='When Edie is being confronted by the hyenas (animalisation) there is a '
                                              'short sequence where there is a high level of abstraction, '
                                              'coupled with the torches, I created a dimly it jungle using back '
                                              'breakups and very dim single source green LED to show positional '
                                              'awareness through lighting.',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea6, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea6, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea6, tag=Scene1)

    idea7 = models.Idea.create_idea(name='Death', content='When it is revealed Edie has died there is a strong change in tension, '
                                             'which I emphasised through a snap change to much colder lighting and '
                                             'strong isolation on his mother center stage.',
                       board=board, colour='#0000ff')
    models.Idea_Tag.create_idea_tag_link(idea=idea7, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea7, tag=Scene1)

    idea8 = models.Idea.create_idea(name='Blood', content='When edie has died on the floor I used rear LED single source red '
                                             'lights which fade up to represent the blood pooling on the floor after '
                                             'being stabbed, this is then referenced in the dialogue.',
                       board=board, colour='#ff0000')
    models.Idea_Tag.create_idea_tag_link(idea=idea8, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea8, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea8, tag=Scene1)

    # Boat
    idea9 = models.Idea.create_idea(name='Boat scene colour', content='In the second scene the setting is on a boat which catches '
                                                         'fire and sinks, to highlight this I used very strong hues '
                                                         'of blue throughout the scene and cold white for face light.',
                       board=board, colour='#0020ff')
    models.Idea_Tag.create_idea_tag_link(idea=idea9, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea9, tag=Scene2)

    idea10 = models.Idea.create_idea(name='Back light', content='In the scene I reflected the tension and senario by using strong '
                                                  'backlight to shilouette the actors as the power is above them - '
                                                  'they have lost control in their death',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea10, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea10, tag=Scene2)

    idea11 = models.Idea.create_idea(name='Representing Boat', content='The blocks which are used throughout the piece as '
                                                         'Complicité would are used in this scene as if the actor '
                                                         'were searching off the helm of the ship shining thee torch '
                                                         'through the haze to her husband she cant see drowning '
                                                         'downstage.',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea11, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea11, tag=Scene2)

    idea12 = models.Idea.create_idea(name='Cloth', content='The blue cloth is used to represent the waves and moved as such, '
                                             'when the waves finally drown the character they shine their torch down '
                                             'the cloth as if they were a dot sinking to the bottom of the sea.',
                       board=board, colour='#0030ff')
    models.Idea_Tag.create_idea_tag_link(idea=idea12, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea12, tag=Scene2)

    # Car
    idea13 = models.Idea.create_idea(name='Abstract crash', content='After the car has crashed the action of crashing is decomposed '
                                                      'and examined in the piece. I wanted to emphasis this by using '
                                                      'void-like lighting, especially from the back, to show again the '
                                                      'lack of power the characters face in their death which they '
                                                      'are searching for the meaning of.',
                       board=board, colour='#ffffff')
    models.Idea_Tag.create_idea_tag_link(idea=idea13, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea13, tag=Scene3)

    idea14 = models.Idea.create_idea(name='LED Lanes', content='When transitioning into this scene the characters use the blocks as '
                                                 'steering wheels for cars and have a little competition in their '
                                                 'driving. I used the LED tape as the lane markings on the road which '
                                                 'gave more context and meaning to their movements, especially when '
                                                 'overtaking.',
                       board=board, colour='#ffffcf')
    models.Idea_Tag.create_idea_tag_link(idea=idea14, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea14, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea14, tag=Scene3)

    idea15 = models.Idea.create_idea(name='Pulses', content='When breaking the crash into 3 stages I wanted to put embassies on '
                                              'the power of the crash even through they were analysing it slowly, '
                                              'when they announced each stage I had a really bright pulse of back '
                                              'light at the audience to show this power and significance in the event.',
                       board=board, colour='#ffffff')
    models.Idea_Tag.create_idea_tag_link(idea=idea15, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea15, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea15, tag=Scene3)

    idea16 = models.Idea.create_idea(name='The death', content='When the crash has been decomposed the organs start to fail, '
                                                 'with each organ I snaped away 1/3 of the light until it was really '
                                                 'dim for the heart to stop (torches used to show heart stopping as a '
                                                 'fist) when it finally snapped to back for the next scene. It '
                                                 'craeted the effect of the body shutting down.',
                       board=board, colour='#111111')
    models.Idea_Tag.create_idea_tag_link(idea=idea16, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea16, tag=Scene3)

    # Train
    idea17 = models.Idea.create_idea(name='Transition into Train', content='For the transition into the train we created a physical '
                                                             'sequence of a train with workers. I brought across this '
                                                             'atmosphere in lighting through back amber lighting from '
                                                             'lights on the floor at the back which lit the haze and '
                                                             'the beams were split by the blocks infront.',
                       board=board, colour='#ff2200')
    models.Idea_Tag.create_idea_tag_link(idea=idea17, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea17, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea17, tag=Scene4)

    idea18 = models.Idea.create_idea(name='Mind the doors', content='For when the doors of the train close there is a moment of '
                                                      'stress which I wanted to portray by a snap transition from '
                                                      'lighting only up stage to mainly lighting mid stage. This was '
                                                      'difficult toisolate in such a small venue, but I used the side '
                                                      'LEDs to emphasise the change',
                       board=board, colour='')
    models.Idea_Tag.create_idea_tag_link(idea=idea18, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea18, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea18, tag=Scene4)

    idea19 = models.Idea.create_idea(name='Running out of Time', content='When the stress of daily life starts to amount the main '
                                                           'character starts to forget what they want to say and '
                                                           'looses communication with the rest of the people. As the '
                                                           'stress intensified I faded up rear blue lights to again '
                                                           'highlight the higher power and add to the '
                                                           'tension/abstraction before snapping to a white void state '
                                                           '(peak tension) before the crash',
                       board=board, colour='#1000ff')
    models.Idea_Tag.create_idea_tag_link(idea=idea19, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea19, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea19, tag=Scene4)

    idea20 = models.Idea.create_idea(name='The crash', content='When the bomb goes off there is a high pitched sound and a sudden '
                                                 'burst of light form the downstage left side parcan with lavender '
                                                 'gel, this then trasnitions into all the side lights and back light '
                                                 'to show the leaast power in the whole piece through the shadows '
                                                 'across the acors faces and sihlouettes from behind. It is meant to '
                                                 'be the most painful moment of the whole piece before snapping back '
                                                 'to the final void.',
                       board=board, colour='#ff2220')
    models.Idea_Tag.create_idea_tag_link(idea=idea20, tag=FixtureType)
    models.Idea_Tag.create_idea_tag_link(idea=idea20, tag=FixtureAngle)
    models.Idea_Tag.create_idea_tag_link(idea=idea20, tag=Scene4)
