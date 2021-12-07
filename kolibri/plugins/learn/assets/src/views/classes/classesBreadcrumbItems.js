import { mapState } from 'vuex';
import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
import { ClassesPageNames } from '../../constants';
import { classAssignmentsLink, lessonPlaylistLink, notificationListLink } from './classPageLinks';

// A mixin intended for use inside of learn plugin breadcrumbs
export default {
  mixins: [commonCoreStrings],
  computed: {
    classesBreadcrumbs() {
      const defaultCrumbs = [
        // Link to All Classes Page
        {
          text: this.coreString('classesLabel'),
          link: {
            name: ClassesPageNames.ALL_CLASSES,
          },
        },
        {
          // Link to Classroom Assignments page
          text: this.currentClassroom.name,
          link: classAssignmentsLink(this.currentClassroom.id),
        },
      ];
      const notificationCrumbs = [
        // Link to All Classes Page
        {
          text: this.coreString('classesLabel'),
          link: {
            name: ClassesPageNames.ALL_CLASSES,
          },
        },
        {
          // Link to Classroom Assignments page
          text: 'Notifications',
          link: classAssignmentsLink(this.currentClassroom.id),
        },
      ];
      const matchupDetailsCrumbs = [
        // Link to All Classes Page
        {
          text: this.coreString('classesLabel'),
          link: {
            name: ClassesPageNames.ALL_CLASSES,
          },
        },
        {
          // Link to Classroom Assignments page
          text: 'Matchup',
          link: classAssignmentsLink(this.currentClassroom.id),
        },
      ];
      switch (this.pageName) {
        case ClassesPageNames.CLASS_ASSIGNMENTS:
          return defaultCrumbs;
        case ClassesPageNames.ALL_NOTIFICATIONS:
          return notificationCrumbs;
        case ClassesPageNames.MATCHUP_DETAILS:
          return matchupDetailsCrumbs;
        case ClassesPageNames.LESSON_PLAYLIST:
          return [
            ...defaultCrumbs,
            {
              // Link to Lesson Playlist
              text: this.currentLesson.title,
              link: lessonPlaylistLink(this.currentLesson.id),
            },
          ];
        default:
          return [];
      }
    },
    showClassesBreadcrumbs() {
      return [
        // No breadcrumbs on ALL_CLASSES or LESSON_RESOURCE_VIEWER
        ClassesPageNames.CLASS_ASSIGNMENTS,
        ClassesPageNames.LESSON_PLAYLIST,
        ClassesPageNames.ALL_NOTIFICATIONS,
        ClassesPageNames.MATCHUP_DETAILS,
      ].includes(this.pageName);
    },
    ...mapState({
      currentClassroom(state) {
        switch (state.pageName) {
          case ClassesPageNames.CLASS_ASSIGNMENTS:
            return state.classAssignments.currentClassroom;
          case ClassesPageNames.LESSON_PLAYLIST:
            return state.lessonPlaylist.currentLesson.classroom;
          default:
            return {};
        }
      },
      currentLesson(state) {
        if (state.pageName === ClassesPageNames.LESSON_PLAYLIST) {
          return state.lessonPlaylist.currentLesson;
        } else {
          return {};
        }
      },
      pageName: state => state.pageName,
    }),
  },
};
